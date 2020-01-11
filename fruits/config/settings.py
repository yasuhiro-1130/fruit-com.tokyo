import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fruit.apps.FruitConfig',
    'django.contrib.humanize',
    'bootstrap4',
    'imagekit',
    'django_cleanup',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# テンプレートの設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
             'builtins':[
                'bootstrap4.templatetags.bootstrap4',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# データベースの設定
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 言語の設定
LANGUAGE_CODE = 'ja'

# タイムゾーンの設定
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# AWS設定
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False

# CloudFrontの設定
AWS_CLOUDFRONT_DOMAIN = 'static.fruit-com.tokyo'

# スタティックファイル(S3)の設定
AWS_STORAGE_BUCKET_NAME = 'fruit-com-static'
STATICFILES_LOCATION = 'static'
STATIC_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = 'config.storage_backends.S3StaticStorageCloudFront'
AWS_DEFAULT_ACL = None

# メディアファイル(S3)の設定
MEDIA_AWS_STORAGE_BUCKET_NAME = 'fruit-com-media'
AWS_S3_MEDIA_URL = '%s.s3.amazonaws.com' % MEDIA_AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_MEDIA_URL, 'media')
DEFAULT_FILE_STORAGE = 'config.storage_backends.S3MediaStorage'
MEDIA_AWS_DEFAULT_ACL = None

# カスタムユーザーモデルの設定
AUTH_USER_MODEL = 'fruit.User'

# ログイン・ログアウトの設定
LOGIN_URL = 'fruit:login'
LOGIN_REDIRECT_URL = 'fruit:item_list'
LOGOUT_REDIRECT_URL = 'fruit:item_list'

# メール送信設定(sendgrid)
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
DEFAULT_FROM_EMAIL = SERVER_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# django.contrib.humanizeの設定(数字を3ケタずつカンマで区切る)
NUMBER_GROUPING = 3

# Stripeの設定
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

