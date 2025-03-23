from datetime import datetime
from http import HTTPStatus

from config import settings
from controllers.models.request import Schedule
from controllers.models.response import (IdScheduleResponse,
                                         IdsScheduleResponse,
                                         NextTakingsResponse,
                                         ReceptionScheduleResponse)
from controllers.responses import ErrorResponse
from database.crud import (create_schedule_controller, get_daily_schedule,
                           get_id_schedules, get_next_taking)
from database.database import get_database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(path="/schedule", summary="Добавить расписание",
             response_model=IdScheduleResponse)
async def create_schedule(schedule: Schedule, session: Session = Depends(get_database)):
    if datetime(year=schedule.treatment_period.year,
                month=schedule.treatment_period.month,
                day=schedule.treatment_period.day) < datetime.now():
        return ErrorResponse(message="Дата из прошлого не может быть установлена!",
                             status_code=HTTPStatus.BAD_REQUEST)
    response = IdScheduleResponse(schedule_id=create_schedule_controller(schedule=schedule, session=session))
    return response


@router.get(path="/schedules", summary="Получить id всех расписаний для пользователя",
            response_model=IdsScheduleResponse)
async def get_schedules(user_id: int, session: Session = Depends(get_database)):
    schedule_list = get_id_schedules(user_id=user_id, session=session)
    if not schedule_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пользователь не найден!")
    response = IdsScheduleResponse(schedule_id_list=schedule_list)
    return response


@router.get(path="/schedule",
            summary="Получить расписание с рассчитанным графиком приема лекарств",
            response_model=ReceptionScheduleResponse)
async def get_daily_schedules(user_id: int, schedule_id: int, session: Session = Depends(get_database)):
    daily_schedule = get_daily_schedule(user_id=user_id, schedule_id=schedule_id, session=session)
    return daily_schedule


@router.get(path="/next_takings", summary="Получить данные о ближайшем приеме лекарств",
            response_model=NextTakingsResponse)
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
