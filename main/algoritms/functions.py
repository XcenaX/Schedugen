from ..models import *

def add_schedule_to_db(schedule):
    """
        Функция добавляет сгенерированное расписание в базу данных
    """
    for group_name, group_schedule in schedule.items():        
        for week_index, _classes in schedule[group_name].items():
            lesson_index = 0
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
    