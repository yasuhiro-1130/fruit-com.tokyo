# Generated by Django 2.2.4 on 2019-10-16 09:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0012_auto_20191016_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='farm_description',
            field=models.TextField(blank=True, max_length=200, verbose_name='農場説明'),
        ),
        migrations.AlterField(
            model_name='farm',
            name='farm_url',
            field=models.CharField(blank=True, max_length=200, validators=[django.core.validators.URLValidator()], verbose_name='ホームページURL'),
        ),
        migrations.AlterField(
            model_name='farmproduct',
            name='product_description',
            field=models.TextField(blank=True, max_length=200, verbose_name='商品説明'),
        ),
    ]
