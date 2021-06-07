from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


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
        ('none', 'Нет'),
        ('white', 'Белый'),
        ('black', 'Чёрный'),
        ('green', 'Зелённый'),
    )

    COUNTRY = (
        ('none', 'Нет'),
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
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Цена')  # Цена
    amount = models.IntegerField(default=0, verbose_name='Кол-во')  # Кол-во
    # min_amount = models.IntegerField(default=3) # Минимальное кол-во
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None', verbose_name='Цвет')  #
    country = models.CharField(max_length=10, choices=COUNTRY, default='None', verbose_name='Страна')  #
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

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def avarege_review(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def count_review(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        cnt_rev = 0
        if reviews["count"] is not None:
            cnt_rev = int(reviews["count"])
        return cnt_rev

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


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


class Comment(models.Model):
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


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate', ]
