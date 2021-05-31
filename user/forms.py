from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label= 'Логин :')
    email = forms.EmailField(max_length=200, label= 'Email :')
    first_name = forms.CharField(max_length=100, label= 'Имя :')
    last_name = forms.CharField(max_length=100, label= 'Фамилия :')
    password1 = forms.CharField(widget = forms.PasswordInput, label = "Пароль")
    password2 = forms.CharField(widget = forms.PasswordInput, label = "Подтвердите пароль")



    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )