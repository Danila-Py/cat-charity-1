from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import donation_crud
from app.crud.base import BaseCharityRepository
from app.models import CharityProject
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investing import distribute_funds

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True
)
async def get_all_donations(
        session: SessionDep
):
    return await donation_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationCreate,
    session: SessionDep,
):
    new_donation = await donation_crud.create(
        donation, session)
    project_repository = BaseCharityRepository(CharityProject)
    return await distribute_funds(new_donation, project_repository, session)