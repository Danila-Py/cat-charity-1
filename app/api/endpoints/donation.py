from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationFullInfoDB,
    DonationDB
)
from app.services.investing import invest_donation


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
    return await invest_donation(new_donation, session)