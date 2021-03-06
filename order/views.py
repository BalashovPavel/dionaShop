from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string


from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product
from user.models import UserProfile


def index(request):
    category = Category.objects.all()
    context = {
        'category':category,
    }
    return HttpResponse("Page order")


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    # product= Product.objects.get(pk=id)

    checkinproduct = ShopCart.objects.filter(product_id=id)  # Check product in shopcart
    if checkinproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""



    if request.method == 'POST':

        # if control == 1:
        #     data = ShopCart.objects.get(product_id=id)
        #     data.quantity += int(request.POST['quantity'])
        #     data.save()
        # else:
        data = ShopCart()
        data.user_id = current_user.id
        data.product_id = id
        data.quantity = int(request.POST['quantity'])
        data.price = int(request.POST['product_price'])
        data.width = int(request.POST['width_rome'])
        data.height = int(request.POST['height_rome'])
        data.save()
        messages.success(request, "Товар добавлен в корзину ")
        return HttpResponseRedirect(url)

    # else:  # if there is no post
    #     if control == 1:  # Update  shopcart
    #         data = ShopCart.objects.get(product_id=id)
    #         data.quantity += 1
    #         data.save()  #
    #     else:  # Inser to Shopcart
    #         data = ShopCart()  # model ile bağlantı kur
    #         data.user_id = current_user.id
    #         data.product_id = id
    #         data.quantity = 1
    #         data.save()  #
    #     messages.success(request, "Product added to Shopcart")
    #     return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    # for rs in shopcart:
    #     rs.quantity = int(request.POST['quantity_in_shopcart'])

    # quantity_shopcart = int(request.POST['quantity_in_shopcart'])
    # print(quantity_shopcart)
    total = 0
    count = shopcart.count()

    for rs in shopcart:
        total += rs.price * rs.quantity

    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'count': count,
        # 'quantity_shopcart': quantity_shopcart,
    }
    return render(request, 'shopcart_products.html', context)

@login_required(login_url='/login')  # Check login
def changefromcart(request, id):
    qty = request.POST['quantity_in_shopcart']
    sets = set(".,:;!_*-+()/#¤%&)").isdisjoint(qty)
    if qty == 0 or qty == '0' or qty == '' or sets == False:
        return HttpResponseRedirect("/shopcart")
    cart_product = ShopCart.objects.get(pk=id)
    cart_product.quantity = qty
    cart_product.save()
    messages.success(request, "Количество товара "+cart_product.product.title+' изменено')
    return HttpResponseRedirect("/shopcart")




@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Товар удалён из корзины")
    return HttpResponseRedirect("/shopcart")


# @login_required(login_url='/login')  # Check login
# def delivery_form(request, id):
#     delivery = request.POST['delivery']
#     # cart_product = ShopCart.objects.get(pk=id)
#     # cart_product.quantity = qty
#     # cart_product.save()
#     # messages.success(request, "Количество товара "+cart_product.product.title+' изменено')
#     return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 200
    for rs in shopcart:
        total += (rs.price * rs.quantity)

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        Order.delivery = request.POST['delivery']
        if Order.delivery == 'Самовывоз':
            total -= 200
        # return HttpResponse(request.POST.items())
        if form.is_valid():

            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.delivery = form.cleaned_data['delivery']
            data.pay = form.cleaned_data['pay']
            data.user_id = current_user.id
            data.total = total
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()  #

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                # if rs.product.variant == 'None':
                detail.price = rs.price
                detail.width = rs.width
                detail.height = rs.height
                # else:
                #     detail.price = rs.variant.price
                # detail.variant_id = rs.variant_id
                detail.amount = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                # if rs.product.variant == 'None':
                product = Product.objects.get(id=rs.product_id)
                # product.amount -= rs.quantity
                product.save()
                # else:
                #     variant = Variants.objects.get(id=rs.product_id)
                #     variant.quantity -= rs.quantity
                #     variant.save()
                # ************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Ваш заказ сохранён")
            return render(request, 'order_completed.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }

    return render(request, 'order_form.html', context)
