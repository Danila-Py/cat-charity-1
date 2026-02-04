from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    """Класс дополнительных методов модели Donation."""


donation_crud = CRUDDonation(Donation)