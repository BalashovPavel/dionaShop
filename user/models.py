from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


# from home.models import Language

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=250, unique=True, verbose_name='Email')
    phone = models.CharField(blank=True, max_length=20, verbose_name='Телефон')
    address = models.CharField(blank=True, max_length=250, verbose_name='Адрес')
    city = models.CharField(blank=True, max_length=50, verbose_name='Город')

    # image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    # def image_tag(self):
    #     return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    # image_tag.short_description = 'Image'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
