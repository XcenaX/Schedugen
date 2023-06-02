from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

# class CustomUser(AbstractUser):
#     pass

WEEK_DAY = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}

# Нагрузка для классов по санпину
WORK_LOAD = {
    "1": {        
        "математика": {
            'workload': 8, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 7, 
            'max_lessons': 2
        },
        "информатика": {
            'workload': 6, 
            'max_lessons': 1
        },
        "природоведение": {
            'workload': 6, 
            'max_lessons': 1
        },
        "русская литература": {
            'workload': 5, 
            'max_lessons': 2
        },
        "история": {
            'workload': 4, 
            'max_lessons': 1
        },
        "рисование": {
            'workload': 3, 
            'max_lessons': 1
        },
        "музыка": {
            'workload': 3, 
            'max_lessons': 1
        },
        "труд": {
            'workload': 2, 
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 1, 
            'max_lessons': 2
        },
    },
    "2": {        
        "математика": {
            'workload': 8,
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 7,
            'max_lessons': 2
        },
        "информатика": {
            'workload': 6,
            'max_lessons': 1
        },
        "природоведение": {
            'workload': 6,
            'max_lessons': 1
        },
        "русская литература": {
            'workload': 5,
            'max_lessons': 2
        },
        "история": {
            'workload': 4,
            'max_lessons': 1
        },
        "рисование": {
            'workload': 3,
            'max_lessons': 1
        },
        "музыка": {
            'workload': 3,
            'max_lessons': 1
        },
        "труд": {
            'workload': 2,
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 1,
            'max_lessons': 2
        },
    },
    "3": {        
        "математика": {
            'workload': 8,
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 7,
            'max_lessons': 2
        },
        "информатика": {
            'workload': 6,
            'max_lessons': 1
        },
        "природоведение": {
            'workload': 6,
            'max_lessons': 1
        },
        "русская литература": {
            'workload': 5,
            'max_lessons': 2
        },
        "история": {
            'workload': 4,
            'max_lessons': 1
        },
        "рисование": {
            'workload': 3,
            'max_lessons': 1
        },
        "музыка": {
            'workload': 3,
            'max_lessons': 1
        },
        "труд": {
            'workload': 2,
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 1,
            'max_lessons': 2
        },
    },
    "4": {        
        "математика": {
            'workload': 8,
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 7,
            'max_lessons': 2
        },
        "информатика": {
            'workload': 6,
            'max_lessons': 1
        },
        "природоведение": {
            'workload': 6,
            'max_lessons': 1
        },
        "русская литература": {
            'workload': 5,
            'max_lessons': 2
        },
        "история": {
            'workload': 4,
            'max_lessons': 1
        },
        "рисование": {
            'workload': 3,
            'max_lessons': 1
        },
        "музыка": {
            'workload': 3,
            'max_lessons': 1
        },
        "труд": {
            'workload': 2,
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 1,
            'max_lessons': 2
        },
    },
    "5":{
        "биология": {
            'workload': 10,
            'max_lessons': 1,
        },
        "математика": {
            'workload': 10,
            'max_lessons': 2,
        },
        "английский язык": {
            'workload': 9,
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 8,
            'max_lessons': 2
        },
        "краеведение": {
            'workload': 7,
            'max_lessons': 1
        },
        "природоведение": {
            'workload': 7,
            'max_lessons': 1
        },
        "граждановедение": {
            'workload': 6,
            'max_lessons': 1
        },
        "история": {
            'workload': 5,
            'max_lessons': 1
        },
        "ритмика": {
            'workload': 4,
            'max_lessons': 1
        },
        "труд": {
            'workload': 4,
            'max_lessons': 1
        },
        "литература": {
            'workload': 4,
            'max_lessons': 2
        },
        "изо": {
            'workload': 3,
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 3,
            'max_lessons': 2
        },
        "экология": {
            'workload': 3,
            'max_lessons': 1
        },
        "музыка": {
            'workload': 2,
            'max_lessons': 1
        },
        "информатика": {
            'workload': 4,
            'max_lessons': 1
        },
        "обж": {
            'workload': 1,
            'max_lessons': 1
        },
    },
    "6":{
        "биология": {
            'workload':8, 
            'max_lessons': 1
        },
        "математика": {
            'workload':13, 
            'max_lessons': 2
        },
        "английский язык": {
            'workload':11, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload':12, 
            'max_lessons': 2
        },
        "краеведение": {
            'workload':9, 
            'max_lessons': 1
        },
        "природоведение": {
            'workload':8, 
            'max_lessons': 1
        },
        "география": {
            'workload':7, 
            'max_lessons': 1
        },
        "граждановедение": {
            'workload':9, 
            'max_lessons': 1
        },
        "история": {
            'workload':8, 
            'max_lessons': 1
        },
        "ритмика": {
            'workload':4, 
            'max_lessons': 1
        },
        "труд": {
            'workload':3, 
            'max_lessons': 1
        },
        "литература": {
            'workload':6, 
            'max_lessons': 2
        },
        "изо": {
            'workload':3, 
            'max_lessons': 1
        },
        "физическая культура": {
            'workload':4, 
            'max_lessons': 2
        },
        "экология": {
            'workload':3, 
            'max_lessons': 1
        },
        "музыка": {
            'workload':1, 
            'max_lessons': 1
        },
        "информатика": {
            'workload':10, 
            'max_lessons': 1
        },
        "обж": {
            'workload':2, 
            'max_lessons': 1
        },
    },
    "7":{
        "химия": {
            'workload': 13, 
            'max_lessons': 1
        },
        "геометрия": {
            'workload': 12, 
            'max_lessons': 2
        },
        "физика": {
            'workload': 8, 
            'max_lessons': 1
        },
        "алгебра": {
            'workload': 10, 
            'max_lessons': 2
        },
        "мировая художественная культура": {
            'workload': 8, 
            'max_lessons': 1
        },
        "биология": {
            'workload': 7, 
            'max_lessons': 1
        },
        "английский язык": {
            'workload': 10, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 11, 
            'max_lessons': 2
        },
        "краеведение": {
            'workload': 5, 
            'max_lessons': 1
        },
        "география": {
            'workload': 6, 
            'max_lessons': 1
        },
        "граждановедение": {
            'workload': 9, 
            'max_lessons': 1
        },
        "история": {
            'workload': 6, 
            'max_lessons': 1
        },
        "труд": {
            'workload': 2, 
            'max_lessons': 1
        },
        "литература": {
            'workload': 4, 
            'max_lessons': 2
        },
        "изо": {
            'workload': 1, 
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 2, 
            'max_lessons': 2
        },
        "экология": {
            'workload': 3, 
            'max_lessons': 1
        },
        "музыка": {
            'workload': 1, 
            'max_lessons': 1
        },
        "информатика": {
            'workload': 4, 
            'max_lessons': 1
        },
        "обж": {
            'workload': 3, 
            'max_lessons': 1
        },
    },
    "8":{
        "химия": {
            'workload': 10, 
            'max_lessons': 1
        },
        "геометрия": {
            'workload': 11, 
            'max_lessons': 1
        },
        "физика": {
            'workload': 9, 
            'max_lessons': 1
        },
        "алгебра": {
            'workload': 9, 
            'max_lessons': 2
        },
        "черчение": {
            'workload': 5, 
            'max_lessons': 1
        },
        "мировая художественная культура": {
            'workload': 5, 
            'max_lessons': 1
        },
        "биология": {
            'workload': 7, 
            'max_lessons': 1
        },
        "английский язык": {
            'workload': 8, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 7, 
            'max_lessons': 2
        },
        "краеведение": {
            'workload': 5, 
            'max_lessons': 1
        },
        "география": {
            'workload': 6, 
            'max_lessons': 1
        },
        "граждановедение": {
            'workload': 5, 
            'max_lessons': 1
        },
        "история": {
            'workload': 8, 
            'max_lessons': 1
        },
        "труд": {
            'workload': 1, 
            'max_lessons': 1
        },
        "литература": {
            'workload': 4, 
            'max_lessons': 2
        },
        "изо": {
            'workload': 3, 
            'max_lessons': 1
        },
        "физическая культура": {
            'workload': 2, 
            'max_lessons': 2
        },
        "экология": {
            'workload': 6, 
            'max_lessons': 1
        },
        "музыка": {
            'workload': 1, 
            'max_lessons': 1
        },
        "информатика": {
            'workload': 7, 
            'max_lessons': 1
        },
        "обж": {
            'workload': 3, 
            'max_lessons': 1
        },
    },
    "9":{
        "химия": {
            'workload': 10, 
            'max_lessons': 1
        },
        "геометрия": {
            'workload': 8, 
            'max_lessons': 2
        },
        "физика": {
            'workload': 11, 
            'max_lessons': 1
        },
        "алгебра": {
            'workload': 7, 
            'max_lessons': 2
        },
        "экономика": {
            'workload': 10, 
            'max_lessons': 1
        },
        "черчение": {
            'workload': 4, 
            'max_lessons': 1
        },
        "мировая художественная культура": {
            'workload': 5, 
            'max_lessons': 1
        },
        "биология": {
            'workload': 7, 
            'max_lessons': 1
        },
        "английский язык": {
            'workload': 9, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 6, 
            'max_lessons': 2
        },
        "география": {
            'workload': 5, 
            'max_lessons': 1
        },
        "история": {
            'workload': 1, 
            'max_lessons': 1
        },
        "труд": {
            'workload': 4, 
            'max_lessons': 1
        },
        "литература": {
            'workload': 7, 
            'max_lessons': 2
        },
        "физическая культура": {
            'workload': 2, 
            'max_lessons': 2
        },
        "экология": {
            'workload': 1, 
            'max_lessons': 1
        },
        "информатика": {
            'workload': 7, 
            'max_lessons': 1
        },
        "обж": {
            'workload': 3, 
            'max_lessons': 1
        },
    },
    "10":{
        "химия": {
            'workload': 11, 
            'max_lessons': 1
        },
        "геометрия": {
            'workload': 11, 
            'max_lessons':2
        },
        "физика": {
            'workload': 12, 
            'max_lessons': 1
        },
        "алгебра": {
            'workload': 10, 
            'max_lessons': 2
        },
        "экономика": {
            'workload': 6, 
            'max_lessons': 1
        },
        "черчение": {
            'workload': 4, 
            'max_lessons': 1
        },
        "мировая художественная культура": {
            'workload': 5, 
            'max_lessons': 1
        },
        "биология": {
            'workload': 7, 
            'max_lessons': 1
        },
        "обществознание": {
            'workload': 5, 
            'max_lessons': 1
        },
        "английский язык": {
            'workload': 8, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 9, 
            'max_lessons': 2
        },
        "география": {
            'workload': 3, 
            'max_lessons': 1
        },
        "история": {
            'workload': 5, 
            'max_lessons': 1
        },
        "труд": {
            'workload': 4, 
            'max_lessons': 1
        },
        "литература": {
            'workload': 8, 
            'max_lessons': 2
        },
        "физическая культура": {
            'workload': 1, 
            'max_lessons': 2
        },
        "экология": {
            'workload': 3, 
            'max_lessons': 1
        },
        "информатика": {
            'workload': 6, 
            'max_lessons': 1
        },
        "обж": {
            'workload': 2, 
            'max_lessons': 1
        },
        "краеведение": {
            'workload': 2, 
            'max_lessons': 1
        },
        "астрономия": {
            'workload': 4, 
            'max_lessons': 1
        },
    },
    "11":{
        "химия": {
            'workload': 11, 
            'max_lessons': 1
        },
        "геометрия": {
            'workload': 11, 
            'max_lessons':2
        },
        "физика": {
            'workload': 12, 
            'max_lessons': 1
        },
        "алгебра": {
            'workload': 10, 
            'max_lessons': 2
        },
        "экономика": {
            'workload': 6, 
            'max_lessons': 1
        },
        "черчение": {
            'workload': 4, 
            'max_lessons': 1
        },
        "мировая художественная культура": {
            'workload': 5, 
            'max_lessons': 1
        },
        "биология": {
            'workload': 7, 
            'max_lessons': 1
        },
        "обществознание": {
            'workload': 5, 
            'max_lessons': 1
        },
        "английский язык": {
            'workload': 8, 
            'max_lessons': 2
        },
        "русский язык": {
            'workload': 9, 
            'max_lessons': 2
        },
        "география": {
            'workload': 3, 
            'max_lessons': 1
        },
        "история": {
            'workload': 5, 
            'max_lessons': 1
        },
        "труд": {
            'workload': 4, 
            'max_lessons': 1
        },
        "литература": {
            'workload': 8, 
            'max_lessons': 2
        },
        "физическая культура": {
            'workload': 1, 
            'max_lessons': 2
        },
        "экология": {
            'workload': 3, 
            'max_lessons': 1
        },
        "информатика": {
            'workload': 6, 
            'max_lessons': 1
        },
        "обж": {
            'workload': 2, 
            'max_lessons': 1
        },
        "краеведение": {
            'workload': 2, 
            'max_lessons': 1
        },
        "астрономия": {
            'workload': 4, 
            'max_lessons': 1
        },
    },
}


class Group(models.Model):
    name = models.CharField(max_length=100)    

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)    

    def __str__(self):
        return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=100, default="Нет имени")    

    def __str__(self):
        return self.name
    
    
class Teacher(models.Model):
    name = models.CharField(max_length=100)            

    def __str__(self):
        return self.name


# Это таблица для составления расписания
class Class(models.Model):
    groups = models.ManyToManyField(Group, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, blank=True, null=True)        
    classrooms = models.ManyToManyField(Classroom, blank=True, null=True)
    max_lessons = models.IntegerField(default=1)
    points = models.IntegerField(default=1)

    def __str__(self):
        groups_str = ""
        for group in self.groups.all():
            groups_str += group.name + ", "
        try:
            return self.subject.name + " | " + groups_str
        except:
            return "Class " + str(self.id)
    

# Это таблица для показа расписания
class ScheduleClass(models.Model):
    weekday = models.IntegerField(default=0)
    lesson_index = models.IntegerField(default=0)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)        
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "weekday": self.weekday,
            "lesson_index": self.weekday,
            "group": self.group.name,
            "teacher": self.teacher.name,
            "subject": self.subject.name,
            "classroom": self.classroom.name,
        }

    def __str__(self):
        return WEEK_DAY[self.weekday] + " | " + str(self.lesson_index) + " урок | " + self.group.name
    

class TestTable(models.Model):
    is_generating = models.BooleanField(default=False)

    def __str__(self):
        return "Is Generating"