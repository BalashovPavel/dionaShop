import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, ProductFilterForm
from home.models import CompanyInformation, ContactForm, ContactMessage, FAQ
from product.models import Product, Category, Images, Review, ProductFilter


def index(request):
    category = Category.objects.all()
    if request.method == 'POST':  # проверка на метож post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # создание связи с моделью
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            # data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # сохранение даных в таблице
            # messages.success(request, 'Благодарим за проявленный интерес, менеджер свяжется с вами в ближайшее время.')
            return HttpResponseRedirect('/home/')

    setting = CompanyInformation.objects.get(pk=1)
    products_slider = Product.objects.all().order_by('-create_at')[:4]
    page = 'home'
    form = ContactForm
    context = {
        'setting': setting,
        'page': page,
        'form': form,
        'products_slider': products_slider,
        'category': category,
    }
    return render(request, 'index.html', context)


def services(request):
    return HttpResponse("services")


def about(request):
    setting = CompanyInformation.objects.get(pk=1)
    category = Category.objects.all()
    context = {
        'setting': setting,
        'category': category,
    }
    return render(request, 'about.html', context)


def delivery(request):
    return HttpResponse("delivery")


# def all_products(request):
#     url = request.META.get('HTTP_REFERER')
#     setting = CompanyInformation.objects.get(pk=1)
#     product = Product.objects.all()
#     category = Category.objects.all()
#     # ordering = request.GET.get('orderby')
#     # review = Review.objects.filter(status=True)
#     # print(review)
#     # if ordering is None:
#     #     product = product.order_by('id')
#     # else:
#     #     product = product.order_by(ordering)
#     order = request.GET.get('order', '-id')
#     product = product.order_by(order)
#     # if order == 'rate':
#     #     product = review.order_by(order)
#     list = []
#     for rs in product:
#
#         list.append(rs.price)
#
#     min_price = min(list)
#     max_price = max(list)
#
#     # feel = request.GET.get('feel')
#     # product = product.filter(feel.qs)
#
#     # form = ProductFilterForm(request.GET)
#     # if form.is_valid():
#     #     if form.cleaned_data["ordering"]:
#     #         product = product.order_by(form.cleaned_data["ordering"])
#
#     filter = ProductFilter(request.GET, queryset=product)
#     paginator = Paginator(filter.qs, 4)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'setting': setting,
#         'product': product,
#         'category': category,
#         'page_obj': page_obj,
#         'filter': filter,
#         'min_price': min_price,
#         'max_price': max_price,
#         # 'ordering': ordering,
#         # 'form': form,
#     }
#     return render(request, 'catalog.html', context)


def all_products(request):
    setting = CompanyInformation.objects.get(pk=1)
    product = Product.objects.all()
    category = Category.objects.all()
    order = request.GET.get('order', '-id')
    product = product.order_by(order)
    list = []
    for rs in product:
        list.append(rs.price)
    min_price = min(list)
    max_price = max(list)
    filter = ProductFilter(request.GET, queryset=product)
    paginator = Paginator(filter.qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'setting': setting,
        'product': product,
        'category': category,
        'page_obj': page_obj,
        'filter': filter,
        'min_price': min_price,
        'max_price': max_price,
        'order': order,
    }
    return render(request, 'catalog.html', context)

# def get_ordering(self):
#     ordering = self.request.GET.get('orderby')
#
#
#     return ordering


def category_products(request, id, slug):

    category = Category.objects.all()
    product = Product.objects.filter(category_id=id)
    if product.count() == 0:
        product = Product.objects.filter(category__parent_id=id)
    catdata = Category.objects.get(pk=id)
    order = request.GET.get('order', '-id')
    product = product.order_by(order)
    list = []
    if product.count() == 0:
        for rs in Product.objects.all():
            list.append(rs.price)
    else:
        for rs in product:
            list.append(rs.price)
    min_price = min(list)
    max_price = max(list)
    filter = ProductFilter(request.GET, queryset=product)
    paginator = Paginator(filter.qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'product': product,
        'category': category,
        'page_obj': page_obj,
        'filter': filter,
        'catdata': catdata,
        'min_price': min_price,
        'max_price': max_price,
        'order': order,
    }
    return render(request, 'catalog.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    catdata = product.category.slug
    images = Images.objects.filter(product_id=id)
    comments = Review.objects.filter(product_id=id, status=True)
    min_width = product.min_width
    min_height = product.min_height
    width_rome = min_width
    height_rome = min_height
    if request.method == 'POST':
        width_rome = int(request.POST['width_rome'])
        height_rome = int(request.POST['height_rome'])
    if catdata == 'rimskie-shtory':
        product_price = int((product.price_rome_cornice * (width_rome / min_width)) + (product.price_rome_cloth * (height_rome / min_height)))
    else:
        product_price = int(
            product.price * (width_rome / min_width))

    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
        'product_price': product_price,
        'width_rome': width_rome,
        'height_rome': height_rome,
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
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            products = Product.objects.filter(title__icontains=search)
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
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        'faq': faq,
        'category': category,
    }
    return render(request, 'faq.html', context)
