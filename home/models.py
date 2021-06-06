from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea


class CompanyInformation(models.Model):
    STATUS = (
        ('Виден', 'Виден'),
        ('Не виден', 'Не виден'),
    )
    title = models.CharField(max_length=250)
    # keywords = models.CharField(max_length=255)
    # description = models.CharField(max_length=255)
    company = models.CharField(max_length=250)
    address = models.CharField(blank=True, max_length=200)
    phone = models.CharField(blank=True, max_length=15)
    # fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=250)
    # smtp_server = models.CharField(blank=True, max_length=50)
    # smtp_email = models.CharField(blank=True, max_length=50)
    # smtp_password = models.CharField(blank=True, max_length=10)
    # smtp_port = models.CharField(blank=True, max_length=5)
    # icon = models.ImageField(blank=True, upload_to='images/')
    # facebook = models.CharField(blank=True, max_length=50)
    vk = models.CharField(blank=True, max_length=250)
    instagram = models.CharField(blank=True, max_length=250)
    # twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=250)
    about_us = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    # references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=False, max_length=20, verbose_name='Имя')
    email = models.CharField(blank=False, max_length=50, verbose_name='Email')
    subject = models.CharField(blank=False, max_length=50)
    message = models.TextField(blank=True, max_length=255, verbose_name='Ваше сообщение')
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            # 'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'input'}),
            'message': Textarea(attrs={'class': 'input', 'rows': '5'}),
        }


class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
