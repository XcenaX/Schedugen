from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class MyUserCreationForm(UserCreationForm):
    login = forms.CharField(max_length=30)

    class Meta:
        model = MyUser
        fields = ('login', 'password')

    def clean_login(self):
        login = self.cleaned_data['login']
        User = get_user_model()
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError("Этот логин уже используется!")
        return login

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 5:
            raise forms.ValidationError("Пароль должен быть не менее 5 символов!")
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError("Ваш пароль слишком простой!")
        return password


class MyAuthenticationForm(AuthenticationForm):
    class Meta():
        model = MyUser
