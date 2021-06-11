from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput

from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='Логин :')
    email = forms.EmailField(max_length=200, label='Email :')
    first_name = forms.CharField(max_length=100, label='Имя :')
    last_name = forms.CharField(max_length=100, label='Фамилия :')
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'Логин'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'city'}),
            # 'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }
