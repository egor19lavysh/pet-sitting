from notifications.views import create_notification

from django.db import models
from datetime import time, timedelta
import datetime
from .models import PetsitterCheck


def filter_objects(model: models.Model, **kwargs):
    return model.objects.filter(**kwargs)



def schedule_report_requests(start_time, interval, frequency, start_date, end_date, for_check: bool = False):
    '''
    The for_check parameter is needed to check the day when the actions were scheduled.
    '''
    time_list = []
    start_datetime = datetime.datetime.combine(start_date, start_time)
    today = datetime.datetime.today()

    for i in range(frequency):
        for j in range(end_date.day - start_date.day + 1):
            task_time = start_datetime + timedelta(days=i, hours=interval * j)

            if not for_check:
                if task_time.date() > today.date():
                    if 5 < task_time.hour < 22:
                        time_list.append(task_time)

                elif task_time.date() == today.date():
                    if task_time.hour > today.hour:
                        if 5 < task_time.hour < 22:
                            time_list.append(task_time)
            else:
                if 5 < task_time.hour < 22:
                    time_list.append(task_time)
    return time_list


def check_report_interval(system: PetsitterCheck, moment: datetime):
    '''
    A function that verifies that the report was sent within a certain verification interval.
    '''
    time_list = schedule_report_requests(
        system.start_time, system.interval, system.frequency, system.start_date, system.end_date, for_check=True)
    now = moment

    in_interval = False

    for task_time in time_list:
        if task_time - timedelta(minutes=30) <= now <= task_time + timedelta(minutes=30):
            in_interval = True
            break

    return in_interval


def update_rest(system: PetsitterCheck):
    '''
    A function that updates rest field of petsitter check system.
    '''

    if system.rest - 1 > 0:
        system.rest -= 1
        system.save()
    elif system.rest - 1 == 0:
        system.status = "SUCCESS"
        system.rest -= 1
        system.save()


def report_request(sitter_id, system_id):
    message = "Загрузите отчет для системы проверки!"
    print("ok")
    create_notification(type="report_load", message=message, user_id =sitter_id, object_id=system_id)
