from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib import messages
from .modules.hashutils import *
import datetime
from django.contrib.auth import authenticate, login, logout
from rest_framework.filters import SearchFilter

from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .modules.utils import *
from .serializers import *
from rest_framework import viewsets

from .algoritms.functions import add_schedule_to_db, get_object_or_404
#
from .algoritms.scheduler import make_schedule

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

            for subject, workload in workloads.items():
                subject_obj = Subject.objects.filter(name__iexact=subject.lower()).first()
                if not get_object_or_404(Subject, name__iexact=subject.lower()):
                    subject_obj = Subject.objects.create(name=subject)
                    subject_obj.save()
                
                
                new_class = Class.objects.create(
                                    subject=subject_obj,
                                    points=workload)
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

            for subject, workload in workloads.items():
                subject_obj = Subject.objects.filter(name__iexact=subject.lower()).first()
                if not Subject.objects.filter(name__iexact=subject.lower()):
                    subject_obj = Subject.objects.create(name=subject)
                    subject_obj.save()
                
                
                new_class = Class.objects.create(
                                    subject=subject_obj,
                                    points=workload)
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


class ScheduleGenerationView(APIView):
    def post(self, request):
        # код составления расписания
        data = Class.objects.all()
        schedule = make_schedule(data)

        ScheduleClass.objects.all().delete()
        add_schedule_to_db(schedule)

        return Response({"message": "Расписание успешно составлено и добавлено в бд", "data": schedule}, status=status.HTTP_200_OK)
        # Если произошла ошибка при составлении расписания
        # return Response({"message": "Произошла ошибка при составлении расписания"}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        # код составления расписания
        data = Class.objects.all()
        schedule = make_schedule(data)

        ScheduleClass.objects.all().delete()
        add_schedule_to_db(schedule)

        return Response({"message": "Расписание успешно составлено и добавлено в бд", "data": schedule}, status=status.HTTP_200_OK)