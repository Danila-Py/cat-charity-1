from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt

from app.schemas.base import BaseDB


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationFullInfoDB(DonationCreate, BaseDB):
    pass


class DonationDB(DonationCreate):
    id: int
    create_date: datetime