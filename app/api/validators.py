from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_project_id_by_name(
        room_name,
        session
    )
    if room_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Благотворительный проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id,
        session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден!'
        )
    return project


async def check_charity_project_before_edit(
        charity_project: CharityProject,
        update_data: CharityProjectUpdate
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать.'
        )
    if (update_data.full_amount and
       update_data.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=400,
            detail='Требуемая сумма не может быть меньше уже внесенной!'
        )
    new_full_amount = update_data.full_amount or charity_project.full_amount
    charity_project.fully_invested = (
        charity_project.invested_amount >= new_full_amount
    )
    if charity_project.fully_invested and not charity_project.close_date:
        from datetime import datetime
        charity_project.close_date = datetime.now()


async def check_charity_project_is_not_invested(
        charity_project: CharityProject
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Нельзя удалить проект с пожертвованиями.'
        )