from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCharityRepository
from app.models import CharityProject, Donation


async def distribute_funds(
    source: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    """Распределяет средства от source к противоположному типу объектов."""
    if isinstance(source, CharityProject):
        target_model = Donation
        source_is_project = True
    else:
        target_model = CharityProject
        source_is_project = False

    repository = BaseCharityRepository(session)
    repository.set_model(target_model)
    targets = await repository.get_active_entities()

    if not targets:
        return source
    available_from_source = source.full_amount - source.invested_amount

    for target in targets:
        if available_from_source <= 0:
            break

        needed_by_target = target.full_amount - target.invested_amount
        to_transfer = min(needed_by_target, available_from_source)

        if to_transfer <= 0:
            continue

        target.invested_amount += to_transfer
        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
        source.invested_amount += to_transfer
        available_from_source -= to_transfer

    if source.invested_amount >= source.full_amount:
        source.fully_invested = True
        source.close_date = datetime.now()
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source


async def invest_donation(
    donation: Donation,
    session: AsyncSession,
) -> Donation:
    """Инвестирует пожертвование в активные проекты."""
    return await distribute_funds(donation, session)


async def invest_to_new_project(
    project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    """Инвестирует в новый проект из активных пожертвований."""
    return await distribute_funds(project, session)