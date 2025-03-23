from datetime import datetime, timedelta
from typing import List


def round_time(date_time: datetime, interval: int) -> datetime:
    """Функция для округления минут во временных метках"""
    discard = timedelta(minutes=date_time.minute % interval,
                        seconds=date_time.second,
                        microseconds=date_time.microsecond)
    date_time -= discard
    if discard >= timedelta(minutes=interval/2):
        date_time += timedelta(minutes=interval)
    return date_time


def calculate_schedule(reception_frequency: int) -> List[datetime]:
    """Функция для расчета графика приема"""
    reception_schedule = []
    current_date = datetime.now().date()
    # разрешенные часы приема с 8 до 22
    delta = timedelta(seconds=14*3600/reception_frequency)
    start_time = datetime(year=current_date.year,
                          month=current_date.month,
                          day=current_date.day,
                          hour=8)
    end_time = datetime(year=current_date.year,
                        month=current_date.month,
                        day=current_date.day,
                        hour=22)
    while start_time < end_time:
        reception_schedule.append(start_time)
        start_time = start_time + delta
    reception_schedule = [round_time(element, 15) for element in reception_schedule]
    return reception_schedule
