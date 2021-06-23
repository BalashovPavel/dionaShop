from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, forms

from product.models import Product


# Create your models here.


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return self.product.title

    # @property
    # def price(self):
    #     return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.price)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity', 'price', 'width', 'height']



class Order(models.Model):
    STATUS = (
        ('Новый', 'Новый'),
        ('Принят', 'Принят'),
        ('Собирается', 'Собирается'),
        ('Передан в доставку', 'Передан в доставку'),
        ('Доставлен', 'Доставлен'),
        ('Отменён', 'Отменён'),
    )

    DELIVERY = (
        ('Курьер', 'Курьер'),
        ('Самовывоз', 'Самовывоз'),
    )

    PAY = (
        ('Картой онлайн', 'Картой онлайн'),
        ('При получении', 'При получении'),

    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, unique=True)
    first_name = models.CharField(blank=False, max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=False, max_length=20)
    email = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=150)
    city = models.CharField(blank=False, max_length=20)
    delivery = models.CharField(blank=False,max_length=20, choices=DELIVERY, default='Курьер')
    pay = models.CharField(blank=False,max_length=50, choices=PAY, default='Картой онлайн')
    total = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='Новый')
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone', 'city', 'email', 'delivery', 'pay']


class OrderProduct(models.Model):
    STATUS = (
        ('Новый', 'Новый'),
        ('Принят', 'Принят'),
        ('Отменён', 'Отменён'),
    )



    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    price = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='Новый')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'
