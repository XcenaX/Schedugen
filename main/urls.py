from django.urls import path
from django.conf.urls import include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    

    path('login', views.LoginView.as_view(), name='login'), 
    path('logout', views.LogoutView.as_view(), name='logout'), 
    path('register', views.RegisterView.as_view(), name='register'),
]