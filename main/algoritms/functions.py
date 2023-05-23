from django.http import Http404
from ..models import *
from django.shortcuts import get_object_or_404
from main.algoritms.costs import WORK_HOURS

def add_schedule_to_db(schedule, second_smena=False):
    """
        Функция добавляет сгенерированное расписание в базу данных
    """
    for group_name, group_schedule in schedule.items():        
        for week_index, _classes in schedule[group_name].items():
            lesson_index = 0
            if second_smena:
                lesson_index = WORK_HOURS
            for _class in _classes:
                if not _class:
                    lesson_index += 1
                    continue
                group = Group.objects.get(name=group_name)
                teacher = Teacher.objects.get(name=_class["teacher"])
                subject = Subject.objects.get(name=_class["subject"])
                classroom = Classroom.objects.get(name=_class["classroom"])

                schedule_class = ScheduleClass.objects.create(weekday=week_index, 
                                            lesson_index=lesson_index,
                                            group=group,
                                            teacher=teacher,
                                            subject=subject,
                                            classroom=classroom)
                schedule_class.save()
                lesson_index += 1


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None