# Generated by Django 2.2.5 on 2019-10-03 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0004_auto_20191003_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name_dlv',
            field=models.CharField(blank=True, max_length=50, verbose_name='お届け先名'),
        ),
    ]
