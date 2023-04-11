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

from django.http import HttpResponseRedirect

from .modules.utils import *

# Create your views here.
class IndexView(View):    
    def get(self, request):        
        return redirect(reverse("main:cabinets"))

    def post(self, request):
        return redirect(reverse("main:cabinets"))


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


class CabinetView(View):    
    template_name = 'admin-panel/cabinets.html'

    def get(self, request):        
        return render(request, self.template_name, {
            
        })

    def post(self, request):
        return render(request, self.template_name, {

        })


class ClassView(View):    
    template_name = 'admin-panel/classes.html'

    def get(self, request):        
        return render(request, self.template_name, {
            
        })

    def post(self, request):
        return render(request, self.template_name, {

        })
    

class SubjectView(View):    
    template_name = 'admin-panel/subjects.html'

    def get(self, request):        
        return render(request, self.template_name, {
            
        })

    def post(self, request):
        return render(request, self.template_name, {

        })
    

class TeacherView(View):    
    template_name = 'admin-panel/teachers.html'

    def get(self, request):        
        return render(request, self.template_name, {
            
        })

    def post(self, request):
        return render(request, self.template_name, {

        })
    

class ScheduleView(View):    
    template_name = 'admin-panel/schedule.html'

    def get(self, request):        
        return render(request, self.template_name, {
            
        })

    def post(self, request):
        return render(request, self.template_name, {

        })