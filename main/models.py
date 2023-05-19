from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

# class CustomUser(AbstractUser):
#     pass

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
    classrooms = models.ManyToManyField(Classroom)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.name


# Это таблица для составления расписания
class Class(models.Model):
    groups = models.ManyToManyField(Group)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    #_type = models.CharField(choices=)
    duration = models.IntegerField(default=1)
    classrooms = models.ManyToManyField(Classroom)
    max_lessons = models.IntegerField(default=1)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.class_name
    

# Это таблица для показа расписания
class ScheduleClass(models.Model):
    weekday = models.IntegerField(default=0)
    lesson_index = models.IntegerField(default=0)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)        
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name
    

class TestTable(models.Model):
    name = models.TextField(default="")

    def __str__(self):
        return self.class_name