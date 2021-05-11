
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS = (
        ('True', 'Виден'),
        ('False', 'Не виден'),
    )
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',
                               on_delete=models.CASCADE)  # отношение "многие к одному"с самим собой
    title = models.CharField(max_length=50)  # Имя категории
    keywords = models.CharField(max_length=255)  # Ключевое слово
    description = models.CharField(max_length=255)  # Описание
    status = models.CharField(max_length=20, choices=STATUS)  # Статус
    image = models.ImageField(blank=True, upload_to='images/')  # Изображение(поле может быть пустым, загружается в)
    slug = models.SlugField()  # Короткая метка
    create_at = models.DateTimeField(auto_now_add=True)  # Создано в
    update_at = models.DateTimeField(auto_now=True)  # Обнавлено в

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS = (
        ('True', 'Виден'),
        ('False', 'Не виден'),
    )

    # VARIANTS = (
    #     ('None', 'None'),
    #     ('Size', 'Size'),
    #     ('Color', 'Color'),
    #     ('Size-Color', 'Size-Color'),
    #
    # )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # отношение "многие к одному" с категорией
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=False)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)  # Цена
    amount = models.IntegerField(default=0)  # Кол-во
    # min_amount = models.IntegerField(default=3) # Минимальное кол-во
    # variant = models.CharField(max_length=10, choices=VARIANTS, default='None') #
    detail = RichTextUploadingField()  # Детали (CKeditor)
    slug = models.SlugField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    ## метод создания фекового поля таблицы в режиме only чтения
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # отношение "многие к одному" с продуктом
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
