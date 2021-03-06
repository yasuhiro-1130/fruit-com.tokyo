# Generated by Django 2.2.5 on 2019-10-03 06:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fruit.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='メールアドレス')),
                ('name', models.CharField(max_length=150, verbose_name='ユーザーネーム')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='名')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='姓')),
                ('postal_code1', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='郵便番号1')),
                ('postal_code2', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='郵便番号2')),
                ('tel_number1', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号1')),
                ('tel_number2', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号2')),
                ('tel_number3', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号3')),
                ('address1', models.CharField(blank=True, max_length=150, verbose_name='住所1')),
                ('address2', models.CharField(blank=True, max_length=150, verbose_name='住所2')),
                ('address3', models.CharField(blank=True, max_length=150, verbose_name='住所3')),
                ('postal_code_dlv1', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='郵便番号1')),
                ('postal_code_dlv2', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='郵便番号2')),
                ('tel_number_dlv1', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号1')),
                ('tel_number_dlv2', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号2')),
                ('tel_number_dlv3', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号3')),
                ('address_dlv1', models.CharField(blank=True, max_length=150, verbose_name='住所1')),
                ('address_dlv2', models.CharField(blank=True, max_length=150, verbose_name='住所2')),
                ('address_dlv3', models.CharField(blank=True, max_length=150, verbose_name='住所3')),
                ('birthday1', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='生年月日1')),
                ('birthday2', models.CharField(blank=True, max_length=2, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='生年月日2')),
                ('birthday3', models.CharField(blank=True, max_length=2, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='生年月日3')),
                ('gender', models.IntegerField(blank=True, choices=[(1, '男性'), (2, '女性'), (3, 'その他')], null=True, verbose_name='性別')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='管理者')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='有効')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'ユーザ',
                'verbose_name_plural': 'ユーザ',
            },
            managers=[
                ('objects', fruit.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_name', models.CharField(max_length=150, verbose_name='農家名')),
                ('farmrep_first_name', models.CharField(blank=True, max_length=30, verbose_name='代表名')),
                ('farmrep_last_name', models.CharField(blank=True, max_length=150, verbose_name='代表姓')),
                ('farm_thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/farm/', verbose_name='農家サムネイル')),
                ('farm_description', models.TextField(blank=True, verbose_name='農家説明')),
                ('farm_address1', models.CharField(blank=True, max_length=150, verbose_name='住所1')),
                ('farm_address2', models.CharField(blank=True, max_length=150, verbose_name='住所2')),
                ('farm_address3', models.CharField(blank=True, max_length=150, verbose_name='住所3')),
                ('farm_tel_number1', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号1')),
                ('farm_tel_number2', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号2')),
                ('farm_tel_number3', models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='電話番号3')),
                ('farm_url', models.TextField(blank=True, max_length=200, validators=[django.core.validators.URLValidator()])),
                ('bank_account', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='口座番号')),
                ('bank_branch_num', models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='支店番号')),
                ('bank_branch_name', models.CharField(blank=True, max_length=20, verbose_name='支店名')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '農家',
                'verbose_name_plural': '農家',
            },
        ),
        migrations.CreateModel(
            name='FarmProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='果物名')),
                ('product_origin', models.CharField(max_length=100, verbose_name='産地名')),
                ('product_description', models.CharField(blank=True, max_length=300, verbose_name='商品説明')),
                ('product_weight', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='商品重量')),
                ('product_stock', models.CharField(max_length=2, validators=[django.core.validators.RegexValidator(message='半角数字で入力して下さい', regex='^[0-9]+$')], verbose_name='商品出荷数')),
                ('product_price', models.IntegerField(verbose_name='商品価格')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='thumbnails/product/', verbose_name='商品サムネイル')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('available', models.BooleanField(default=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit.Farm')),
            ],
            options={
                'verbose_name': '農作物',
                'verbose_name_plural': '農作物',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='数量')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='fruit.ShoppingCart', verbose_name='ショッピングカート')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit.FarmProduct', verbose_name='商品')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, verbose_name='評価')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('comment', models.TextField(blank=True, verbose_name='コメント')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='fruit.FarmProduct', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
