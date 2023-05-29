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

    path('generate', views.ScheduleGenerationView.as_view(), name='generate'), 
    path('initial_workload', views.SanPinInitialDataView.as_view(), name='initial_workload'),
    path('random_setup_teachers', views.RandomlySetupTeachers.as_view(), name='random_setup_teachers'),
    path('is_generating', views.IsGeneratingView.as_view(), name='is_generating'),
    path('generate_general_data', views.GenerateGeneralData.as_view(), name='generate_general_data'),
    
    
    path('login', views.LoginView.as_view(), name='login'), 
    path('logout', views.LogoutView.as_view(), name='logout'), 
    path('register', views.RegisterView.as_view(), name='register'),
]