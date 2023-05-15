from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models    

class MyUserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(password=password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #school = models.ForeignKey(School, on_delete=models.CASCADE)

    objects = MyUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

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