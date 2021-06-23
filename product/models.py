import django_filters
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Avg, Count
from django.forms import ModelForm, CheckboxSelectMultiple
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_filters import filters
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from django.forms.widgets import HiddenInput


class Category(MPTTModel):
    STATUS = (
        ('True', 'Виден'),
        ('False', 'Не виден'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children',
                            on_delete=models.CASCADE)  # отношение "многие к одному"с самим собой
    title = models.CharField(max_length=50, verbose_name='Наименование')  # Имя категории
    keywords = models.CharField(max_length=255, verbose_name='Ключевое слово')  # Ключевое слово
    description = models.CharField(max_length=255, verbose_name='Описание')  # Описание
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='Статус видимости')  # Статус
    image = models.ImageField(blank=True, upload_to='images/',
                              verbose_name='Изображение категории')  # Изображение(поле может быть пустым, загружается в)
    slug = models.SlugField(null=False, unique=True, verbose_name='Короткая метка')  # Короткая метка
    create_at = models.DateTimeField(auto_now_add=True)  # Создано в
    update_at = models.DateTimeField(auto_now=True)  # Обнавлено в

    def __str__(self):
        return self.title

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    STATUS = (
        ('True', 'Виден'),
        ('False', 'Не виден'),
    )

    VARIANTS = (
        ('white', 'Белый'),
        ('black', 'Чёрный'),
        ('green', 'Зелённый'),
    )

    COUNTRY = (
        ('turkey', 'Турция'),
        ('russia', 'Россия'),
        ('china', 'Китай'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория')  # отношение "многие к одному" с категорией
    title = models.CharField(max_length=150, verbose_name='Название')
    keywords = models.CharField(max_length=255, verbose_name='Ключевое слово')
    description = models.CharField(max_length=255, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', null=False, verbose_name='Изображение')
    price_rome_cornice = models.IntegerField(default=0, verbose_name='Цена римского карниза', null=True)
    price_rome_cloth = models.IntegerField(default=0, verbose_name='Цена ткани для римскиой шторы', null=True)
    price = models.IntegerField( default=0, verbose_name='Цена товара', null=False)
    min_width = models.IntegerField( verbose_name='Минимальная ширина (см.)')
    max_width = models.IntegerField( verbose_name='Максимальная ширина (см.)')
    min_height = models.IntegerField( verbose_name='Минимальная высота (см.)')
    max_height = models.IntegerField( verbose_name='Максимальная высота (см.)')
    rate = models.DecimalField( verbose_name='Рейтинг товара', default=0, max_digits=2, decimal_places=1)
    # amount = models.IntegerField(default=0, verbose_name='Кол-во')  # Кол-во
    # min_amount = models.IntegerField(default=3) # Минимальное кол-во
    color = models.CharField(max_length=10, choices=VARIANTS, verbose_name='Цвет')  #
    country = models.CharField(max_length=10, choices=COUNTRY, verbose_name='Страна производства')  #
    detail = RichTextUploadingField(verbose_name='Детали')  # Детали (CKeditor)
    slug = models.SlugField(null=False, unique=True, verbose_name='Метка')
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='Статус')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # метод создания фекового поля таблицы в режиме only чтения
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


    def article(self):
        if self.id is not None:
            return f'{self.category_id:03}'+'/'+f'{self.id:03}'


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def avarege_review(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
            self.rate = avg
            self.save(update_fields=["rate"])
        if reviews["avarage"] is None:
            self.rate = 0
        return self.rate


    def count_review(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        cnt_rev = 0
        if reviews["count"] is not None:
            cnt_rev = int(reviews["count"])
        return cnt_rev

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        # ordering = ['id']


# class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass


class ProductFilter(django_filters.FilterSet):
    country = filters.MultipleChoiceFilter(field_name='country', choices=Product.COUNTRY, widget=CheckboxSelectMultiple)
    variant = filters.MultipleChoiceFilter(field_name='color', choices=Product.VARIANTS, widget=CheckboxSelectMultiple)
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['price', 'variant', 'country']


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Продукт')  # отношение "многие к одному" с продуктом
    title = models.CharField(max_length=50, blank=True, verbose_name='Название')
    image = models.ImageField(blank=True, upload_to='images/', verbose_name='Изображение')

    def __str__(self):
        return self.title

    # метод создания фекового поля таблицы в режиме only чтения
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    class Meta:
        verbose_name = 'Дополнительное изображение'
        verbose_name_plural = 'Изображения доп.'


class Review(models.Model):
    STATUS = (
        ('New', 'Новый'),
        ('True', 'Виден'),
        ('False', 'Не виден'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Продукт')  # отношение "многие к одному" с продуктом
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Логин')
    subject = models.CharField(max_length=50, blank=True, verbose_name='Субъект')
    comment = models.CharField(max_length=500, blank=True, verbose_name='Отзыв')
    rate = models.IntegerField(default=5, verbose_name='Оценка')
    ip = models.CharField(max_length=20, blank=True, verbose_name='IP')
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='Статус', default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'comment', 'rate', ]
