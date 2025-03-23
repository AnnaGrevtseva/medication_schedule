from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config import settings
from controllers.models.request import Schedule
from controllers.responses import ErrorResponse
from database.database import get_database
from database.crud import create_schedule_controller, get_id_schedules, get_daily_schedule, get_next_taking

router = APIRouter()


@router.post(path="/schedule", summary="Добавить расписание")
async def create_schedule(schedule: Schedule, session: Session = Depends(get_database)):
    if datetime(year=schedule.treatment_period.year,
                month=schedule.treatment_period.month,
                day=schedule.treatment_period.day) < datetime.now():
        return ErrorResponse(message="Дата из прошлого не может быть установлена!",
                             status_code=HTTPStatus.BAD_REQUEST)
    return create_schedule_controller(schedule=schedule, session=session)


@router.get(path="/schedules/{user_id}", summary="Получить id всех расписаний для пользователя")
async def get_schedules(user_id: int, session: Session = Depends(get_database)):
    schedule_list = get_id_schedules(user_id=user_id, session=session)
    if not schedule_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пользователь не найден!")
    return {"schedules_id": schedule_list}


@router.get(path="/schedule/{user_id}/{schedule_id}",
            summary="Получить расписание с рассчитанным графиком приема лекарств")
async def get_daily_schedules(user_id: int, schedule_id: int, session: Session = Depends(get_database)):
    daily_schedule = get_daily_schedule(user_id=user_id, schedule_id=schedule_id, session=session)
    return daily_schedule


@router.get(path="/next_takings/{user_id}", summary="Получить данные о ближайшем приеме лекарств")
async def get_next_takings(user_id: int, session: Session = Depends(get_database)):
    next_takings = get_next_taking(user_id=user_id, session=session)
    if type(next_takings) is list:
        if next_takings:
            return {f'В течение {settings.NEXT_TAKINGS} минут есть прием лекарств': next_takings}
        else:
            return ErrorResponse(message=f"Для пользователя {user_id} не найдено ближайших приемов!",
                                status_code=HTTPStatus.NOT_FOUND)
    else:
        return next_takings
