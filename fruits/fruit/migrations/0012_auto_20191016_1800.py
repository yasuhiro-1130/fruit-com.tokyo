# Generated by Django 2.2.4 on 2019-10-16 09:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0011_auto_20191016_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='farmproduct',
            name='product_description',
            field=models.CharField(blank=True, max_length=200, verbose_name='商品説明'),
        ),
        migrations.AlterField(
            model_name='farmproduct',
            name='product_name',
            field=models.CharField(max_length=20, verbose_name='果物名'),
        ),
    ]
