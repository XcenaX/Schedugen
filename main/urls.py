from django.urls import path
from django.conf.urls import include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    
    path('cabinets', views.CabinetView.as_view(), name='cabinets'), 
    path('classes', views.ClassView.as_view(), name='classes'), 
    path('subjects', views.SubjectView.as_view(), name='subjects'), 
    path('teachers', views.TeacherView.as_view(), name='teachers'), 
    path('schedule', views.ScheduleView.as_view(), name='schedule'), 

    path('login', views.LoginView.as_view(), name='login'), 
    path('logout', views.LogoutView.as_view(), name='logout'), 
    path('register', views.RegisterView.as_view(), name='register'),
]