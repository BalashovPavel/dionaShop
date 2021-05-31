from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from user.forms import SignUpForm
from user.models import UserProfile


def index(request):
    return HttpResponse("hello")


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)

            return HttpResponseRedirect("/")
        else:
            messages.warning(request,"Введён неверный Логин или Пароль")

            return HttpResponseRedirect("/login")
    return render(request, 'login_form.html')

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.email = current_user.email
            # data.image="images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')


    form = SignUpForm()
    #category = Category.objects.all()
    context = {#'category': category,
               'form': form,
               }
    return render(request, 'signup_form.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")