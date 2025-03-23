from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List, Tuple

from config import settings
from controllers.models.request import Schedule
from controllers.models.response import ReceptionScheduleResponse
from controllers.responses import ErrorResponse
from database.models import ScheduleDb
from database.useful import calculate_schedule
from fastapi import HTTPException
from sqlalchemy.orm import Session


def create_schedule_controller(schedule: Schedule, session: Session) -> int:
    """Функция для создания расписаний"""
    schedule_data = ScheduleDb(drug_name=schedule.drug_name,
                               reception_frequency=schedule.reception_frequency,
                               treatment_period=schedule.treatment_period,
                               user_id=schedule.user_id)
    session.add(schedule_data)
    session.commit()
    session.refresh(schedule_data)
    return schedule_data.schedule_id


def get_id_schedules(user_id: int, session: Session) -> List[int]:
    """Функция возвращает идентификаторы расписаний для указанного пользователя"""
    db_data = session.query(ScheduleDb.schedule_id).filter(ScheduleDb.user_id == user_id).all()
    schedule_id_list = []
    for elem in db_data:
        schedule_id_list.append(*elem)
    return schedule_id_list


def get_daily_schedule(user_id: int, schedule_id: int, session: Session) -> ReceptionScheduleResponse:
    """Функция предоставляет инфо о выбранном расписании с графиком приема лекарств"""
    available_schedules = get_id_schedules(user_id=user_id, session=session)
    if not available_schedules:
        return ErrorResponse(message="Пользователь не найден!",
                             status_code=HTTPStatus.NOT_FOUND)
    if schedule_id in available_schedules:
        db_data = (session.query(ScheduleDb.drug_name,
                                 ScheduleDb.treatment_period,
                                 ScheduleDb.reception_frequency).
                                 filter(ScheduleDb.schedule_id == schedule_id).first())
        drug_name, treatment_period, reception_frequency = db_data
        current_date = datetime.now().date()
        if current_date > treatment_period:
            return ErrorResponse(message=f"Период приема лекарства {drug_name} завершен!",
                                 status_code=HTTPStatus.OK)
        else:
            reception_schedule = calculate_schedule(reception_frequency=reception_frequency)
            response = ReceptionScheduleResponse(drug_name=drug_name,
                                                 treatment_period=treatment_period,
                                                 reception_frequency=reception_frequency,
                                                 reception_schedule=reception_schedule)
            return response
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Расписание не найдено!")


def get_next_taking(user_id: int, session: Session) -> List[Tuple]:
    """Функция предоставляет инфо о ближайшем приеме лекарств для указанного пользователя"""
    next_taking_list = []
    near_period = settings.NEXT_TAKINGS
    available_schedules = get_id_schedules(user_id=user_id, session=session)
    if not available_schedules:
        return ErrorResponse(message="Пользователь не найден!",
                             status_code=HTTPStatus.NOT_FOUND)
    for schedule in available_schedules:
        response = get_daily_schedule(user_id=user_id, schedule_id=schedule, session=session)
        if type(response) is ReceptionScheduleResponse:
            current_date = datetime.now()
            near_period_date = current_date + timedelta(seconds=60*near_period)
            reception_schedule = response.reception_schedule
            for time_point in reception_schedule:
                if current_date <= time_point <= near_period_date:
                    next_taking_list.append((response.drug_name,
                                             f"Дата окончания приема: {response.treatment_period}",
                                             f"Ближайший прием лекарства: {time_point}"))

    return next_taking_list


















