# Generated by Django 3.2.2 on 2021-06-11 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_contactmessage_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='subject',
        ),
    ]
