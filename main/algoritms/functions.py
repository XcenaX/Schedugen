from django.http import Http404
from ..models import *
from django.shortcuts import get_object_or_404
from main.algoritms.costs import WORK_HOURS

def add_schedule_to_db(data, matrix, second_smena=False):
    """
        Функция добавляет сгенерированное расписание в базу данных
    """
    len_y = len(matrix)
    len_x = len(matrix[0])
    for i in range(len_y):        
        for j in range(len_x):
            if matrix[i][j] is None:
                continue                        
            
            _class = data.classes[matrix[i][j]]
            
            if not _class:                
                continue

            group = None
            for group_name, group_id in data.groups.items():
                if group_id == _class.groups[0]:
                    group = Group.objects.get(name=group_name)
                    break

            teacher = Teacher.objects.get(name=_class.teacher)
            subject = Subject.objects.get(name=_class.subject)
            classroom = Classroom.objects.get(name=_class.classroom)

            lesson_index = (i+1) % WORK_HOURS
            if second_smena:
                lesson_index += WORK_HOURS

            schedule_class = ScheduleClass.objects.create(weekday=i // WORK_HOURS, 
                                        lesson_index=lesson_index,
                                        group=group,
                                        teacher=teacher,
                                        subject=subject,
                                        classroom=classroom)
            schedule_class.save()
            


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None