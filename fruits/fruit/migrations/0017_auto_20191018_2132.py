# Generated by Django 2.2.4 on 2019-10-18 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0016_auto_20191018_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='farm',
            options={'verbose_name': '農場', 'verbose_name_plural': '農場'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '注文', 'verbose_name_plural': '注文'},
        ),
        migrations.AlterModelOptions(
            name='ordereditem',
            options={'verbose_name': '注文商品', 'verbose_name_plural': '注文商品'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'コメント', 'verbose_name_plural': 'コメント'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'ショッピングカート', 'verbose_name_plural': 'ショッピングカート'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcartitem',
            options={'verbose_name': 'ショッピングカートアイテム', 'verbose_name_plural': 'ショッピングカートアイテム'},
        ),
    ]
