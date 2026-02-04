from datetime import datetime

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_donation(
    donation: Donation,
    session: AsyncSession,
) -> Donation:
    remaining_amount = donation.full_amount - donation.invested_amount
    projects = await get_active_projects(session)

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
    donations = await get_active_donations(session)
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


async def get_active_projects(
    session: AsyncSession
):
    active_projects = await session.execute(
        select(CharityProject)
        .where(
            CharityProject.close_date.is_(None),
            CharityProject.fully_invested.is_(False),
        )
        .order_by(asc(CharityProject.create_date))
    )
    return active_projects.scalars().all()


async def get_active_donations(
    session: AsyncSession
):
    donations = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(asc(Donation.create_date))
    )
    return donations.scalars().all()