import threading
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from main.forms import *
from main.models import *
from django.contrib import messages
from main.modules.hashutils import *
import datetime
from django.contrib.auth import authenticate, login, logout
from rest_framework.filters import SearchFilter

from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from main.modules.utils import *
from main.serializers import *
from rest_framework import viewsets

from main.algoritms.functions import add_schedule_to_db, get_object_or_404
#
from main.algoritms.scheduler import do_add, get_index, make_schedule, PERVYA_SMENA, VTORAYA_SMENA, schedule_to_dict
from main.algoritms.costs import WORK_HOURS, get_schedule_for_groups, WORK_DAYS
import asyncio

from asgiref.sync import sync_to_async

from django.db import close_old_connections

class RegisterView(View):
    form_class = MyUserCreationForm
    template_name = 'registration/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    form_class = MyAuthenticationForm


    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ScheduleClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScheduleClass.objects.all()
    serializer_class = ScheduleClassSerializer


class SanPinInitialDataView(APIView):
    def post(self, request):
        # для ускорения заполнения всех полей тут добавляются все самые основные данные оп санпину
        Class.objects.all().delete()

        for class_number, workloads in WORK_LOAD.items():
            groups = []
            for group in Group.objects.all():
                if group.name.startswith(class_number) and class_number.__len__() + 1 == group.name.__len__():
                    groups.append(group)
                        
            if not groups:
                continue

            for subject, subject_data in workloads.items():
                subject_obj = Subject.objects.filter(name__iexact=subject.lower()).first()
                if not get_object_or_404(Subject, name__iexact=subject.lower()):
                    subject_obj = Subject.objects.create(name=subject)
                    subject_obj.save()
                
                print(subject_data)
                
                new_class = Class.objects.create(
                                    subject=subject_obj,
                                    points=subject_data["workload"],
                                    max_lessons=subject_data["max_lessons"])
                for group in groups:
                    new_class.groups.add(group)
                for classroom in Classroom.objects.all():
                    new_class.classrooms.add(classroom)
                new_class.save()

        return Response({"message": "Успешно!"}, status=status.HTTP_200_OK)
        
    def get(self, request):
        # для ускорения заполнения всех полей тут добавляются все самые основные данные оп санпину
        Class.objects.all().delete()
        
        for class_number, workloads in WORK_LOAD.items():
            groups = []
            for group in Group.objects.all():
                if group.name.startswith(class_number) and class_number.__len__() + 1 == group.name.__len__():
                    groups.append(group)
            print(groups)

            if not groups:
                continue

            for subject, subject_data in workloads.items():
                subject_obj = Subject.objects.filter(name__iexact=subject.lower()).first()
                if not Subject.objects.filter(name__iexact=subject.lower()):
                    subject_obj = Subject.objects.create(name=subject)
                    subject_obj.save()
                
                
                new_class = Class.objects.create(
                                    subject=subject_obj,
                                    points=subject_data["workload"],
                                    max_lessons=subject_data["max_lessons"])
                for group in groups:
                    new_class.groups.add(group)
                for classroom in Classroom.objects.all():
                    new_class.classrooms.add(classroom)
                new_class.save()
                



        return Response({"message": "Успешно!"}, status=status.HTTP_200_OK)
        # Если произошла ошибка при составлении расписания
        # return Response({"message": "Произошла ошибка при составлении расписания"}, status=status.HTTP_400_BAD_REQUEST)


class RandomlySetupTeachers(APIView):
    def get(self, request):
        # рандомно раскидывает учителей по предметам, нужно для тестов        
        teachers = Teacher.objects.all()
        subjects = Subject.objects.all()
        index = 0
        for subject in subjects:
            classes = Class.objects.filter(subject=subject)
            for _class in classes:
                _class.teacher = teachers[index % len(teachers)]
                _class.save()
            index += 1


        return Response({"message": "Успешно!"}, status=status.HTTP_200_OK)

class GenerateGeneralData(APIView):
    def get(self, request):
        # generating some groups
        letters = ["А", "Б", "В", "Г"]
        for index in range(1, 12):
            for letter in letters:
                group = Group.objects.create(name="{0}{1}".format(index, letter))
                group.save()
        
        # generating some classrooms
        count_floors = 4
        classrooms_per_floor = 10
        for floor in range(1, count_floors+1):
            for number in range(1, classrooms_per_floor+1):
                if len(str(number)) == 1: 
                    number = "0{0}".format(number)
                classroom = Classroom.objects.create(name="{0}{1}".format(floor, number))
                classroom.save()

        #generating some teachers 
        count_teachers = 20
        for index in range(1, count_teachers+1):
            teacher = Teacher.objects.create(name="Учитель {0}".format(index))
            teacher.save()

        return Response({"message": "Успешно!"}, status=status.HTTP_200_OK)


class ScheduleGenerationView(APIView):
    
    def schedule(self):
        first_smena_groups = []
        second_smena_groups = []
        for group in Group.objects.all():
            for f_group_index in PERVYA_SMENA:
                if group.name.startswith(f_group_index) and f_group_index.__len__() + 1 == group.name.__len__():
                    first_smena_groups.append(group)
            for s_group_index in VTORAYA_SMENA:
                if group.name.startswith(s_group_index) and s_group_index.__len__() + 1 == group.name.__len__():
                    second_smena_groups.append(group)
    
        first_group_ids = [group.id for group in first_smena_groups]
        second_group_ids = [group.id for group in second_smena_groups]
        
        # Получаем все уроки для первой и второй смены
        first_smena = Class.objects.filter(groups__id__in=first_group_ids).distinct()    
        second_smena = Class.objects.filter(groups__id__in=second_group_ids).distinct()        

        
        schedule_first, data1 = make_schedule(first_smena, first_smena_groups)
        # schedule_first_dict = schedule_to_dict(schedule_first, data)
        schedule_second, data2 = make_schedule(second_smena, second_smena_groups)

        print("SCHEDULE READY... ADDING TO DB")

        for schedule_class in ScheduleClass.objects.all():
            schedule_class.delete()

        # close_old_connections()
        add_schedule_to_db(data1, schedule_first)
        add_schedule_to_db(data2, schedule_second, True)
        
        _ = TestTable.objects.all().first()
        _.is_generating = False
        _.save()

        print("FUCK YE")
        
        return schedule_first, schedule_second, data1, data2
            
    def post(self, request):
        _ = TestTable.objects.all().first()
        _.is_generating = True
        _.save()

        # loop = asyncio.get_event_loop()
        # task = loop.create_task(self.schedule())
        # self.schedule()
        # t = threading.Thread(target=self.schedule, args=(), kwargs={})
        # t.daemon = False
        # t.start()
        self.schedule()

        return Response({"message": "Расписание началось генерироваться!"}, status=status.HTTP_200_OK)  
        

class IsGeneratingView(APIView):
    def get(self, request):
        if TestTable.objects.all().first() is None:
            _  = TestTable.objects.create()
            _.save()
        return Response({"is_generating": TestTable.objects.all().first().is_generating}, status=status.HTTP_200_OK)       


class TestView(APIView):
    def get(self, request):     
        classes = ScheduleClass.objects.all()
        groups = Group.objects.all()
        classes_dict = {}
        for group in groups:
            classes_dict[group.name] = {}
            for i in range(5):
                classes_dict[group.name][i] = {}
                for j in range(14):
                    classes_dict[group.name][i][j] = {}

        for c in classes:            
            classes_dict[c.group.name][c.weekday][c.lesson_index] = {
                "classroom": c.classroom.name,
                "teacher": c.teacher.name,
                "subject": c.subject.name,
            }

        

        #print(classes_dict)

        return render(request, "admin-panel/test.html", {
            "groups": groups,
            "classes": classes_dict,
            "lessons": range(14)
        })
    

class MistakesView(APIView):
    def get(self, request):    
        classes = ScheduleClass.objects.all()
        # groups = Group.objects.all()
        mistakes = []
        
        for i in range(WORK_DAYS):
            for j in range(WORK_HOURS):
                row = classes.filter(weekday=i, lesson_index=j)
                classrooms_set = set()
                teachers_set = set()                
                index = 0    
                for row_class in row:                     
                       
                    
                    if do_add(classrooms_set, row_class.classroom.name) is False:                            
                        # error_class2 = row[index]
                        error_class = None
                        for item in row:
                            if row_class.classroom.name == item.classroom.name:
                                error_class = item
                                break
                        mistakes.append({
                            "messageType": "Пересечение кабинетов",
                            "message": "У {0} и {1} классов одинаковые кабинеты. {2} {3} урок".format(error_class.group.name, row_class.group.name, WEEK_DAY[i], j+1),
                            "classes": [error_class.to_dict(), row_class.to_dict()]
                        })                            
                        

                    if do_add(teachers_set, row_class.teacher.name) is False:                            
                        # error_class2 = row[index]
                        error_class = None
                        for item in row:
                            if row_class.teacher.name == item.teacher.name:
                                error_class = item
                                break
                        mistakes.append({
                            "messageType": "Пересечение учителей",
                            "message": "У {0} и {1} классов одинаковые учителя. {2} {3} урок".format(error_class.group.name, row_class.group.name, WEEK_DAY[i], j+1),
                            "classes": [error_class.to_dict(), row_class.to_dict()]
                        }) 

                    index += 1                                               

        return Response({"mistakes": mistakes}, status=status.HTTP_200_OK)       