import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage, FAQ
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

# def product_detail(request,id,slug):
#     query = request.GET.get('q')
#     # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
#     defaultlang = settings.LANGUAGE_CODE[0:2] #en-EN
#     currentlang = request.LANGUAGE_CODE[0:2]
#     #category = categoryTree(0, '', currentlang)
#     category = Category.objects.all()
#
#     product = Product.objects.get(pk=id)
#
#     if defaultlang != currentlang:
#         try:
#             prolang =  Product.objects.raw('SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
#                                           'FROM product_product as p '
#                                           'INNER JOIN product_productlang as l '
#                                           'ON p.id = l.product_id '
#                                           'WHERE p.id=%s and l.lang=%s',[id,currentlang])
#             product=prolang[0]
#         except:
#             pass
#     # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end
#
#     images = Images.objects.filter(product_id=id)
#     comments = Comment.objects.filter(product_id=id,status='True')
#     context = {'product': product,'category': category,
#                'images': images, 'comments': comments,
#                }
#     if product.variant !="None": # Product have variants
#         if request.method == 'POST': #if we select color
#             variant_id = request.POST.get('variantid')
#             variant = Variants.objects.get(id=variant_id) #selected product by click color radio
#             colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
#             sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
#             query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
#         else:
#             variants = Variants.objects.filter(product_id=id)
#             colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
#             sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
#             variant =Variants.objects.get(id=variants[0].id)
#         context.update({'sizes': sizes, 'colors': colors,
#                         'variant': variant,'query': query
#                         })
#     return render(request,'product_detail.html',context)



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


# def search_auto(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         products = Product.objects.filter(title__icontains=q)
#         results = []
#         for rs in products:
#             product_json = {}
#             product_json = rs.title
#             results.append(product_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)


def faq(request):
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        'faq': faq,
    }
    return render(request, 'faq.html', context)