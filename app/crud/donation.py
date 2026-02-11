from app.crud.base import BaseCharityRepository
from app.models.donation import Donation


class CRUDDonation(BaseCharityRepository):
    """Класс дополнительных методов модели Donation."""


donation_crud = CRUDDonation(Donation)