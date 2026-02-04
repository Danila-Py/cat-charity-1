from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.crud.base import BaseCharityRepository


async def invest_donation(
    donation: Donation,
    session: AsyncSession,
) -> Donation:
    """
    Инвестирует пожертвование в активные проекты.

    Args:
        donation (Donation): Пожертвование для инвестирования.
        session (AsyncSession): Сессия базы данных.

    Returns:
        Donation: Обновленное пожертвование.
    """
    remaining_amount = donation.full_amount - donation.invested_amount
    repository = BaseCharityRepository(session)
    projects = await repository.get_active_projects()

    for project in projects:
        needed_amount = project.full_amount - project.invested_amount
        to_invest = min(needed_amount, remaining_amount)

        project.invested_amount += to_invest
        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()

        donation.invested_amount += to_invest
        remaining_amount -= to_invest

    if donation.invested_amount == donation.full_amount:
        donation.fully_invested = True
        donation.close_date = datetime.now()
    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


async def invest_to_new_project(
    project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    """
    Инвестирует в новый проект из активных пожертвований.

    Args:
        project (CharityProject): Проект для инвестирования.
        session (AsyncSession): Сессия базы данных.
    """
    repository = BaseCharityRepository(session)
    donations = await repository.get_active_donations()
    if not donations:
        return project
    remaining_needed = project.full_amount - project.invested_amount
    for donation in donations:
        available_amount = donation.full_amount - donation.invested_amount
        to_invest = min(available_amount, remaining_needed)
        donation.invested_amount += to_invest
        if donation.invested_amount >= donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
        project.invested_amount += to_invest
        remaining_needed -= to_invest
    if project.invested_amount >= project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project