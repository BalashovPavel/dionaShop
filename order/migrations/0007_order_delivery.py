# Generated by Django 3.2.2 on 2021-06-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210610_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.CharField(choices=[('Курьер', 'Курьер'), ('Самовывоз', 'Самовывоз')], default='Курьер', max_length=20),
        ),
    ]
