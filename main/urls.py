from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'classrooms', views.ClassroomViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'classes', views.ClassViewSet)
router.register(r'schedule-classes', views.ScheduleClassViewSet)

app_name= "main"
urlpatterns = [
    path('', include(router.urls)),
    path('login', views.LoginView.as_view(), name='login'), 
    path('logout', views.LogoutView.as_view(), name='logout'), 
    path('register', views.RegisterView.as_view(), name='register'),
]