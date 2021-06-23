# Generated by Django 3.2.2 on 2021-06-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_rename_comment_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='country',
            field=models.CharField(choices=[('turkey', 'Турция'), ('russia', 'Россия'), ('china', 'Китай')], max_length=10, verbose_name='Страна производства'),
        ),
    ]
