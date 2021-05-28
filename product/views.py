from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from product.models import CommentForm, Comment


def index(request):
    return HttpResponse('I AM PRODUCT')


def addcomment(request, id):
    url = request.META.get('HTTP_REFERER') # получение ur адреса
    if request.method == 'POST':  # проверка на метож post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # создание связи с моделью
            # data.name = form.cleaned_data['name']
            # data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            # current_user = request.user
            # return HttpResponse(request.user)
            data.user = request.user
            data.save()  # сохранение даных в таблице
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)
