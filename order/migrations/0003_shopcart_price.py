# Generated by Django 3.2.2 on 2021-06-09 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210607_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
