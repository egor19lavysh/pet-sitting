from notifications.views import create_notification
from django.db import models
from datetime import time, timedelta
import datetime
from .models import PetsitterCheck

from typing import List, Union
from datetime import datetime, time, date, timedelta

def is_valid_hour(hour: int) -> bool:
    """Проверка, что время в допустимом интервале (6:00 - 21:59)"""
    return 6 <= hour < 22

def schedule_report_requests(
    obj: PetsitterCheck, 
    for_check: bool = False
) -> List[datetime]:
    """Генерирует список временных меток для отчетов.
    
    Args:
        obj: Объект PetsitterCheck или словарь с параметрами.
        for_check: Игнорировать текущее время при генерации.
    """

    params = {
            "start_time": obj.start_time,
            "interval": obj.interval,
            "frequency": obj.frequency,
            "start_date": obj.start_date,
            "end_date": obj.end_date,
        }
    
    start_datetime = datetime.combine(params["start_date"], params["start_time"])
    today = datetime.now()
    time_list = []

    total_days = (params["end_date"] - params["start_date"]).days + 1

    for day in range(total_days):
        current_date = params["start_date"] + timedelta(days=day)
        for attempt in range(params["frequency"]):
            task_time = start_datetime + timedelta(
                days=day,
                hours=params["interval"] * attempt
            )
            
            if not is_valid_hour(task_time.hour):
                continue
                
            if not for_check:
                if task_time.date() > today.date():
                    time_list.append(task_time)
                elif task_time.date() == today.date() and task_time.time() > today.time():
                    time_list.append(task_time)
            else:
                time_list.append(task_time)

    return sorted(time_list)


def is_time_in_interval(
    target_time: datetime, 
    check_time: datetime, 
    margin: timedelta = timedelta(minutes=30)
) -> bool:
    """Проверяет, попадает ли check_time в интервал target_time ± margin."""
    return (target_time - margin) <= check_time <= (target_time + margin)

def check_report_interval(system: PetsitterCheck, moment: datetime) -> bool:
    time_list = schedule_report_requests(system, for_check=True)
    return any(is_time_in_interval(task_time, moment) for task_time in time_list)

def report_request(sitter_id: int, system_id: int) -> None:
    try:
        message = f"Загрузите отчет для системы проверки #{system_id}"
        create_notification(
            type="report_load",
            message=message,
            user_id=sitter_id,
            object_id=system_id
        )
    except Exception as e:
        print(f"Ошибка создания уведомления: {str(e)}") # Загатовка под логгирование


