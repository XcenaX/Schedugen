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

from algoritms.scheduler import main as make_schedule


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
    template_name = 'registration/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

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
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ScheduleClassViewSet(viewsets.ModelViewSet):
    queryset = ScheduleClass.objects.all()
    serializer_class = ScheduleClassSerializer


class ScheduleGenerationView(APIView):
    def post(self, request):
        # код составления расписания
        data = Class.objects.all()
        schedule = make_schedule(data)
        return Response({"message": "Расписание успешно составлено"}, status=status.HTTP_200_OK)
        # Если произошла ошибка при составлении расписания
        # return Response({"message": "Произошла ошибка при составлении расписания"}, status=status.HTTP_400_BAD_REQUEST)