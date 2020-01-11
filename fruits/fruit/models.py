from django.db import models
from django.conf import settings

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator, URLValidator
from django.db.models import F, Sum, Avg, IntegerField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.functions import Cast


class MyUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'

    email = models.EmailField(
        'メールアドレス',
        max_length=150,
        null=False,
        blank=False,
        unique=True,
    )

    name = models.CharField(
        'ユーザーネーム',
        max_length=150,
        null=False,
        blank=False,
    )

    first_name = models.CharField(
        _('名'),
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        _('姓'),
        max_length=150,
        blank=True,
    )

    postal_code_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=("半角数字で入力して下さい"),
    )

    postal_code1 = models.CharField(
        validators=[postal_code_regex],
        max_length=3,
        verbose_name='郵便番号1',
        blank=True,
    )

    postal_code2 = models.CharField(
        validators=[postal_code_regex],
        max_length=4,
        verbose_name='郵便番号2',
        blank=True,
    )

    tel_number_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=("半角数字で入力して下さい"),
    )

    tel_number1 = models.CharField(
        validators=[tel_number_regex],
        max_length=3,
        verbose_name='電話番号1',
        blank=True,
    )

    tel_number2 = models.CharField(
        validators=[tel_number_regex],
        max_length=4,
        verbose_name='電話番号2',
        blank=True,
    )

    tel_number3 = models.CharField(
        validators=[tel_number_regex],
        max_length=4,
        verbose_name='電話番号3',
        blank=True,
    )

    address1 = models.CharField(
        _('住所1'),
        max_length=150,
        blank=True,
    )

    address2 = models.CharField(
        _('住所2'),
        max_length=150,
        blank=True,
    )

    address3 = models.CharField(
        _('住所3'),
        max_length=150,
        blank=True,
    )

    name_dlv = models.CharField(
        _('お届け先名'),
        max_length=50,
        blank=True,
    )

    postal_code_dlv1 = models.CharField(
        validators=[postal_code_regex],
        max_length=3,
        verbose_name='郵便番号1',
        blank=True,
    )

    postal_code_dlv2 = models.CharField(
        validators=[postal_code_regex],
        max_length=4,
        verbose_name='郵便番号2',
        blank=True,
    )

    tel_number_dlv1 = models.CharField(
        validators=[tel_number_regex],
        max_length=3,
        verbose_name='電話番号1',
        blank=True,
    )

    tel_number_dlv2 = models.CharField(
        validators=[tel_number_regex],
        max_length=4,
        verbose_name='電話番号2',
        blank=True,
    )

    tel_number_dlv3 = models.CharField(
        validators=[tel_number_regex],
        max_length=4,
        verbose_name='電話番号3',
        blank=True,
    )

    address_dlv1 = models.CharField(
        _('住所1'),
        max_length=150,
        blank=True,
    )

    address_dlv2 = models.CharField(
        _('住所2'),
        max_length=150,
        blank=True,
    )

    address_dlv3 = models.CharField(
        _('住所3'),
        max_length=150,
        blank=True,
    )

    YEAR_CHOICES = (
        ("1900", 1900),
        ("1901", 1901),
        ("1902", 1902),
        ("1903", 1903),
        ("1904", 1904),
        ("1905", 1905),
        ("1906", 1906),
        ("1907", 1907),
        ("1908", 1908),
        ("1909", 1909),
        ("1910", 1910),
        ("1911", 1911),
        ("1912", 1912),
        ("1913", 1913),
        ("1914", 1914),
        ("1915", 1915),
        ("1916", 1916),
        ("1917", 1917),
        ("1918", 1918),
        ("1919", 1919),
        ("1920", 1920),
        ("1921", 1921),
        ("1922", 1922),
        ("1923", 1923),
        ("1924", 1924),
        ("1925", 1925),
        ("1926", 1926),
        ("1927", 1927),
        ("1928", 1928),
        ("1929", 1929),
        ("1930", 1930),
        ("1931", 1931),
        ("1932", 1932),
        ("1933", 1933),
        ("1934", 1934),
        ("1935", 1935),
        ("1936", 1936),
        ("1937", 1937),
        ("1938", 1938),
        ("1939", 1939),
        ("1940", 1940),
        ("1941", 1941),
        ("1942", 1942),
        ("1943", 1943),
        ("1944", 1944),
        ("1945", 1945),
        ("1946", 1946),
        ("1947", 1947),
        ("1948", 1948),
        ("1949", 1949),
        ("1950", 1950),
        ("1951", 1951),
        ("1952", 1952),
        ("1953", 1953),
        ("1954", 1954),
        ("1955", 1955),
        ("1956", 1956),
        ("1957", 1957),
        ("1958", 1958),
        ("1959", 1959),
        ("1960", 1960),
        ("1961", 1961),
        ("1962", 1962),
        ("1963", 1963),
        ("1964", 1964),
        ("1965", 1965),
        ("1966", 1966),
        ("1967", 1967),
        ("1968", 1968),
        ("1969", 1969),
        ("1970", 1970),
        ("1971", 1971),
        ("1972", 1972),
        ("1973", 1973),
        ("1974", 1974),
        ("1975", 1975),
        ("1976", 1976),
        ("1977", 1977),
        ("1978", 1978),
        ("1979", 1979),
        ("1980", 1980),
        ("1981", 1981),
        ("1982", 1982),
        ("1983", 1983),
        ("1984", 1984),
        ("1985", 1985),
        ("1986", 1986),
        ("1987", 1987),
        ("1988", 1988),
        ("1989", 1989),
        ("1990", 1990),
        ("1991", 1991),
        ("1992", 1992),
        ("1993", 1993),
        ("1994", 1994),
        ("1995", 1995),
        ("1996", 1996),
        ("1997", 1997),
        ("1998", 1998),
        ("1999", 1999),
        ("2000", 2000),
        ("2001", 2001),
        ("2002", 2002),
        ("2003", 2003),
        ("2004", 2004),
        ("2005", 2005),
        ("2006", 2006),
        ("2007", 2007),
        ("2008", 2008),
        ("2009", 2009),
        ("2010", 2010),
        ("2011", 2011),
        ("2012", 2012),
        ("2013", 2013),
        ("2014", 2014),
        ("2015", 2015),
        ("2016", 2016),
        ("2017", 2017),
        ("2018", 2018),
        ("2019", 2019),
        ("2020", 2020),
        ("2021", 2021),
        ("2022", 2022),
        ("2023", 2023),
        ("2024", 2024),
        ("2025", 2025),
        ("2026", 2026),
        ("2027", 2027),
        ("2028", 2028),
        ("2029", 2029),
        ("2030", 2030),
    )
    birthday1 = models.CharField(
        choices=YEAR_CHOICES,
        max_length=4,
        verbose_name='生年月日1',
        blank=True,
    )

    MONTH_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("11", 11),
        ("12", 12),
    )
    birthday2 = models.CharField(
        choices=MONTH_CHOICES,
        max_length=2,
        verbose_name='生年月日2',
        blank=True,
    )

    DAY_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("11", 11),
        ("12", 12),
        ("13", 13),
        ("14", 14),
        ("15", 15),
        ("16", 16),
        ("17", 17),
        ("18", 18),
        ("19", 19),
        ("20", 20),
        ("21", 21),
        ("22", 22),
        ("23", 23),
        ("24", 24),
        ("25", 25),
        ("26", 26),
        ("27", 27),
        ("28", 28),
        ("29", 29),
        ("30", 30),
        ("31", 31),
    )
    birthday3 = models.CharField(
        choices=DAY_CHOICES,
        max_length=2,
        verbose_name='生年月日3',
        blank=True,
    )

    GENDER_CHOICES = (
        ('男性', '男性'),
        ('女性', '女性'),
        ('その他', 'その他'),
    )
    gender = models.CharField(
        verbose_name='性別',
        choices=GENDER_CHOICES,
        max_length=3,
        blank=True,
    )

    is_staff = models.BooleanField(
        '管理者',
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        '有効', default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'), )

    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def email_user(self, subject, message, from_email=None, **kwargs):

        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email

    @property
    def order_count(self):
        return self.orders.all().count()


class Farm(models.Model):
    class Meta:
        verbose_name = '農場'
        verbose_name_plural = '農場'

    farm_name = models.CharField(
        verbose_name='農場名',
        max_length=20,
        null=False,
        blank=False,
    )

    farmrep_first_name = models.CharField(
        _('代表名'),
        max_length=20,
        blank=True,
    )

    farmrep_last_name = models.CharField(
        _('代表姓'),
        max_length=20,
        blank=True,
    )

    farm_image = models.ImageField(
        verbose_name='農家サムネイル',
        upload_to="thumbnails/farm/",
        blank=True,
        null=True,
    )

    farm_description = models.TextField(
        verbose_name='農場説明',
        max_length=200,
        blank=True,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    farm_postal_code_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=("半角数字で入力して下さい"),
    )

    farm_postal_code1 = models.CharField(
        validators=[farm_postal_code_regex],
        max_length=3,
        verbose_name='郵便番号1',
        blank=True,
    )

    farm_postal_code2 = models.CharField(
        validators=[farm_postal_code_regex],
        max_length=4,
        verbose_name='郵便番号2',
        blank=True,
    )

    farm_address1 = models.CharField(
        _('住所1'),
        max_length=150,
        blank=True,
    )

    farm_address2 = models.CharField(
        _('住所2'),
        max_length=150,
        blank=True,
    )

    farm_address3 = models.CharField(
        _('住所3'),
        max_length=150,
        blank=True,
    )

    tel_number_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=("半角数字で入力して下さい"),
    )

    farm_tel_number1 = models.CharField(
        validators=[tel_number_regex],
        max_length=3,
        verbose_name='電話番号1',
        blank=True,
    )

    farm_tel_number2 = models.CharField(
        validators=[tel_number_regex],
        max_length=4,
        verbose_name='電話番号2',
        blank=True,
    )

    farm_tel_number3 = models.CharField(
        validators=[tel_number_regex],
        max_length=4,
        verbose_name='電話番号3',
        blank=True,
    )

    bank_num_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=("半角数字で入力して下さい"),
    )

    farm_url = models.CharField(
        validators=[URLValidator()],
        blank=True,
        verbose_name='ホームページURL',
        max_length=200,
    )

    bank_name = models.CharField(
        max_length=20,
        verbose_name='金融機関名',
        blank=True,
    )

    bank_account = models.CharField(
        validators=[bank_num_regex],
        max_length=7,
        verbose_name='口座番号',
        blank=True,
    )

    bank_branch_num = models.CharField(
        validators=[bank_num_regex],
        max_length=3,
        verbose_name='支店番号',
        blank=True,
    )

    bank_branch_name = models.CharField(
        max_length=20,
        verbose_name='支店名',
        blank=True,
    )


class FarmProduct(models.Model):
    class Meta:
        verbose_name = '果物'
        verbose_name_plural = '果物'

    product_name = models.CharField(
        verbose_name='果物名',
        max_length=20,
        null=False,
        blank=False,
    )

    PRODUCT_CATEGORY_CHOICES = (
        ("杏", "杏"),
        ("いちご", "いちご"),
        ("いちじく", "いちじく"),
        ("梅", "梅"),
        ("柿", "柿"),
        ("オレンジ", "オレンジ"),
        ("グレープフルーツ", "グレープフルーツ"),
        ("ゆず", "ゆず"),
        ("みかん", "みかん"),
        ("レモン", "レモン"),
        ("その他柑橘類", "その他柑橘類"),
        ("キウイフルーツ", "キウイフルーツ"),
        ("さくらんぼ", "さくらんぼ"),
        ("スイカ", "スイカ"),
        ("プラム", "プラム"),
        ("洋梨", "洋梨"),
        ("梨", "梨"),
        ("パイナップル", "パイナップル"),
        ("バナナ", "バナナ"),
        ("パパイア", "パパイア"),
        ("ビワ", "ビワ"),
        ("ぶどう", "ぶどう"),
        ("ブルーベリー", "ブルーベリー"),
        ("クランベリー", "クランベリー"),
        ("ラズベリー", "ラズベリー"),
        ("マスカット", "マスカット"),
        ("マンゴー", "マンゴー"),
        ("メロン", "メロン"),
        ("桃", "桃"),
        ("りんご", "りんご"),
        ("プルーン", "プルーン"),
        ("ネクタリン", "ネクタリン"),
        ("その他", "その他"),
    )
    product_category = models.CharField(
        verbose_name='カテゴリー名',
        choices=PRODUCT_CATEGORY_CHOICES,
        max_length=10,
        null=False,
        blank=False,
    )

    PRODUCT_ORIGIN_CHOICES = (
        ("北海道産", "北海道"),
        ("青森県産", "青森県"),
        ("岩手県産", "岩手県"),
        ("宮城県産", "宮城県"),
        ("秋田県産", "秋田県"),
        ("山形県産", "山形県"),
        ("福島県産", "福島県"),
        ("茨城県産", "茨城県"),
        ("栃木県産", "栃木県"),
        ("群馬県産", "群馬県"),
        ("埼玉県産", "埼玉県"),
        ("千葉県産", "千葉県"),
        ("東京都産", "東京都"),
        ("神奈川県産", "神奈川県"),
        ("新潟県産", "新潟県"),
        ("富山県産", "富山県"),
        ("石川県産", "石川県"),
        ("福井県産", "福井県"),
        ("山梨県産", "山梨県"),
        ("長野県産", "長野県"),
        ("岐阜県産", "岐阜県"),
        ("静岡県産", "静岡県"),
        ("愛知県産", "愛知県"),
        ("三重県産", "三重県"),
        ("滋賀県産", "滋賀県"),
        ("京都府産", "京都府"),
        ("大阪府産", "大阪府"),
        ("兵庫県産", "兵庫県"),
        ("奈良県産", "奈良県"),
        ("和歌山県産", "和歌山県"),
        ("鳥取県産", "鳥取県"),
        ("島根県産", "島根県"),
        ("岡山県産", "岡山県"),
        ("広島県産", "広島県"),
        ("山口県産", "山口県"),
        ("徳島県産", "徳島県"),
        ("香川県産", "香川県"),
        ("愛媛県産", "愛媛県"),
        ("高知県産", "高知県"),
        ("福岡県産", "福岡県"),
        ("佐賀県産", "佐賀県"),
        ("長崎県産", "長崎県"),
        ("熊本県産", "熊本県"),
        ("大分県産", "大分県"),
        ("宮崎県産", "宮崎県"),
        ("鹿児島県産", "鹿児島県"),
        ("沖縄県産", "沖縄県"),
    )
    product_origin = models.CharField(
        verbose_name='産地名',
        max_length=5,
        choices=PRODUCT_ORIGIN_CHOICES,
        null=False,
        blank=False,
    )

    product_description = models.TextField(
        verbose_name='商品説明',
        max_length=250,
        blank=True,
    )

    PRODUCT_WEIGHT_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("11", 11),
        ("12", 12),
        ("13", 13),
        ("14", 14),
        ("15", 15),
        ("16", 16),
        ("17", 17),
        ("18", 18),
        ("19", 19),
        ("20", 20),
        ("21", 21),
        ("22", 22),
        ("23", 23),
        ("24", 24),
        ("25", 25),
        ("26", 26),
        ("27", 27),
        ("28", 28),
        ("29", 29),
        ("30", 30),
        ("31", 31),
        ("32", 32),
        ("33", 33),
        ("34", 34),
        ("35", 35),
        ("36", 36),
        ("37", 37),
        ("38", 38),
        ("39", 39),
        ("40", 40),
        ("41", 41),
        ("42", 42),
        ("43", 43),
        ("44", 44),
        ("45", 45),
        ("46", 46),
        ("47", 47),
        ("48", 48),
        ("49", 49),
        ("50", 50),
    )
    product_weight = models.CharField(
        max_length=3,
        choices=PRODUCT_WEIGHT_CHOICES,
        verbose_name='商品重量',
        blank=False,
    )

    PRODUCT_STOCK_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("11", 11),
        ("12", 12),
        ("13", 13),
        ("14", 14),
        ("15", 15),
        ("16", 16),
        ("17", 17),
        ("18", 18),
        ("19", 19),
        ("20", 20),
    )
    product_stock = models.CharField(
        max_length=2,
        choices=PRODUCT_STOCK_CHOICES,
        verbose_name='商品出荷数',
        blank=False,
    )

    price_num_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=("半角数字で入力して下さい"),
    )
    product_price = models.CharField(
        verbose_name='商品価格',
        validators=[price_num_regex],
        max_length=6,
        blank=False,
    )

    product_image = models.ImageField(
        verbose_name='商品画像',
        upload_to='images/',
        blank=True,
        null=True,
    )

    thumbnail = ImageSpecField(source='product_image',
                               processors=[ResizeToFill(760, 600)],
                               format="JPEG",
                               options={'quality': 60},
                               )

    big = ImageSpecField(source='product_image',
                         processors=[ResizeToFill(900, 640)],
                         format="JPEG",
                         options={'quality': 100},
                         )

    small = ImageSpecField(source='product_image',
                           processors=[ResizeToFill(75, 75)],
                           format="JPEG",
                           options={'quality': 50},
                           )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    available = models.BooleanField(
        default=True,
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
    )

    @property
    def avg_rating(self):
        return self.reviews.all().aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0


class ShoppingCart(models.Model):
    class Meta:
        verbose_name = 'ショッピングカート'
        verbose_name_plural = 'ショッピングカート'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='ショッピングカートユーザ',
        related_name='cart',
        on_delete=models.CASCADE,
    )

    @property
    def item_count(self):
        # PostgreSQL8.3以降、フィールドの型がWHERE句の処理時等に厳密にチェックされるため、ShoppingCartItemクラスのamountの型を集計前にIntegerに変換する処理を含む
        return self.cart_items.all().annotate(
            as_integer=Cast(
                'amount', IntegerField())).aggregate(
            amount=Sum('as_integer'))['amount']

    @property
    def total_amount(self):
        # PostgreSQL8.3以降、フィールドの型がWHERE句の処理時等に厳密にチェックされるため、ShoppingCartItemクラスのamountとproduct_priceの型を集計前にIntegerに変換する処理を含む
        return self.cart_items.all().annotate(
            as_price=Cast(
                'product__product_price',
                IntegerField())).annotate(
            as_amount=Cast(
                'amount',
                IntegerField())).aggregate(
                    total=Sum(
                        F('as_price') * F('as_amount'),
                        output_field=IntegerField()))['total']


class ShoppingCartItem(models.Model):
    class Meta:
        verbose_name = 'ショッピングカートアイテム'
        verbose_name_plural = 'ショッピングカートアイテム'

    cart = models.ForeignKey(
        ShoppingCart,
        related_name='cart_items',
        verbose_name='ショッピングカート',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        FarmProduct,
        verbose_name='ショッピングカート商品',
        on_delete=models.CASCADE,
    )

    CART_ITEM_AMOUNT_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("11", 11),
        ("12", 12),
        ("13", 13),
        ("14", 14),
        ("15", 15),
        ("16", 16),
        ("17", 17),
        ("18", 18),
        ("19", 19),
        ("20", 20),
    )
    amount = models.CharField(
        verbose_name='ショッピングカート数量',
        max_length=2,
        choices=CART_ITEM_AMOUNT_CHOICES,
    )

    @property
    def sub_total_amount(self):
        return int(self.product.product_price) * int(self.amount)


class Review(models.Model):
    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'

    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        FarmProduct,
        related_name='reviews',
        verbose_name='商品',
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        verbose_name='評価',
        default=0
    )

    comment = models.TextField(
        verbose_name='コメント',
        blank=True,
        max_length=200,
    )

    created = models.DateTimeField(
        verbose_name='コメント作成日時',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        verbose_name='コメント更新日時',
        auto_now=True,
    )


class Order(models.Model):
    class Meta:
        verbose_name = '注文'
        verbose_name_plural = '注文'

    user = models.ForeignKey(
        User,
        related_name='orders',
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    is_shipped = models.BooleanField(
        '発送フラグ', default=False
    )

    is_settled = models.BooleanField(
        '決済フラグ', default=False
    )

    stripe_id = models.CharField(
        'stripe_id', max_length=200
    )

    created_at = models.DateTimeField(
        '注文日付', default=timezone.now
    )

    @property
    def total_amount(self):
        # PostgreSQL8.3以降、フィールドの型がWHERE句の処理時等に厳密にチェックされるため、OrderedItemクラスのamountとproduct_priceの型を集計前にIntegerに変換する処理を含む
        return self.ordered_items.all().annotate(
            as_price=Cast(
                'product__product_price',
                IntegerField())).annotate(
            as_amount=Cast(
                'amount',
                IntegerField())).aggregate(
                    total=Sum(
                        F('as_price') * F('as_amount'),
                        output_field=IntegerField()))['total']


class OrderedItem(models.Model):
    class Meta:
        verbose_name = '注文商品'
        verbose_name_plural = '注文商品'

    order = models.ForeignKey(
        Order,
        related_name='ordered_items',
        verbose_name='注文',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        FarmProduct,
        verbose_name='注文商品',
        on_delete=models.CASCADE,
    )

    amount = models.CharField(
        verbose_name='注文数量',
        max_length=2,
    )
