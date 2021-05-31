import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage
from product.models import Product, Category, Images, Comment


def index(request):
    if request.method == 'POST':  # проверка на метож post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # создание связи с моделью
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # сохранение даных в таблице
            messages.success(request, 'Благодарим за проявленный интерес, менеджер свяжется с вами в ближайшее время.')
            return HttpResponseRedirect('/home/')

    setting = Setting.objects.get(pk=1)
    products_slider = Product.objects.all().order_by('-id')[:4]
    page = 'home'
    form = ContactForm
    context = {
        'setting': setting,
        'page': page,
        'form': form,
        'products_slider': products_slider,
    }
    return render(request, 'index.html', context)


def services(request):
    return HttpResponse("services")


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {
        'setting': setting
    }
    return render(request, 'about.html', context)


def delivery(request):
    return HttpResponse("delivery")


def all_products(request):
    setting = Setting.objects.get(pk=1)
    product = Product.objects.all()
    category = Category.objects.all()
    context = {
        'setting': setting,
        'product': product,
        'category': category,
    }
    return render(request, 'catalog.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    context = {
        'products': products,
        'category': category,
        'catdata': catdata,
    }
    return render(request, 'catalog.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status=True)
    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
    }
    return render(request, 'product_detail.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']  # get form input data
            products = Product.objects.filter(
                title__icontains=search)  # SELECT * FROM product WHERE title LIKE '%query%'
            category = Category.objects.all()
            context = {
                'products': products,
                'search': search,
                'category': category
            }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



