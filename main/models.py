from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
class SchoolClass(models.Model):
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student')
    max_lessons_per_day = models.IntegerField(default=6)
    max_lessons_per_week = models.IntegerField(default=30)

    def __str__(self):
        return self.class_name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    room_number = models.CharField(max_length=100)

    def __str__(self):
        return self.room_number

class Lesson(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    day = models.CharField(max_length=100)
    time = models.TimeField()

    def __str__(self):
        return f'{self.teacher} - {self.school_class} ({self.classroom})'
    

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