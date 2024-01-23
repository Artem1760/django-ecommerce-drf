from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

# Environmental variables
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG', cast=bool)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'jazzmin',  # admin view   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'core.apps.CoreConfig',
    'account.apps.AccountConfig',
    'book.apps.BookConfig',
    'cart.apps.CartConfig',
    'checkout.apps.CheckoutConfig',
    'rest_api.apps.RestApiConfig',
    # Custom Filters
    'book.templatetags.custom_filters',

    # Third party packages    
    'crispy_forms',
    'crispy_tailwind',
    'taggit',  # used for tags
    'ckeditor',
    # text editor allows users to write content directly inside admin page.

    # Third party API packages  
    'algoliasearch_django',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',  # make my API available for other domains 
    'djoser',  # drf token auth

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'core.context_processors.default',
                'cart.context_processors.cart',

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom_prj.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#  PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': env.db('DB_ENGINE'),
#         'NAME': env.db('DB_NAME'),
#         'USER': env.db('DB_USER'),
#         'PASSWORD': env.db('DB_PASSWORD'),
#         'PORT': env.db('DB_PORT'),
#         'HOST': env.list('DB_HOST'),
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static_files']
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User model
AUTH_USER_MODEL = 'account.CustomerUser'

LOGIN_REDIRECT_URL = 'core:index'  # when we logged in it sends us to lead_list page
LOGIN_URL = 'account:login'  # when we try to get access to permitted pages -> when we are not logged in a page with LoginMixin will take us to the login page
LOGOUT_REDIRECT_URL = 'account:login'

CRISPY_TEMPLATE_PACK = 'tailwind'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

EMAIL_HOST = env.list('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Basket session ID
CART_SESSION_ID = 'cart'

# JAZZMIN
JAZZMIN_SETTINGS = {
    'site_title': _('Molla'),
    'site_header': _('Molla Administration'),
    'site_brand': _('Molla'),
    'site_logo': 'assets/images/logo.png',
    'welcome_sign': _('Welcome to Molla Administration'),
    'site_copyrights': 'my-shop.com',
    'search_model': ['auth.User', 'auth.Group'],
    'topmenu_links': [
        {'name': _('Home'), 'url': 'admin:index',
         'permissions': ['auth.view_user']},
        {'model': 'auth.User'},
        {'app': 'books'},
    ],
}

# ckeditor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document',
             'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print',
                       '-', 'Templates']},
            {'name': 'clipboard',
             'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                       '-', 'Undo', 'Redo']},
            {'name': 'editing',
             'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
                       'Select', 'Button', 'ImageButton',
                       'HiddenField']}, '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                       'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent',
                       'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                       'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley',
                       'SpecialChar', 'PageBreak', 'Iframe']}, '/',
            {'name': 'styles',
             'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']}, '/',
            {'name': 'yourcustomtools', 'items': [
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

TAGGIT_CASE_INSENSITIVE = True

# Paypal
PAYPAL_RECEIVER_EMAIL = env('PAYPAL_RECEIVER_EMAIL')
PAYPAL_TEST = env('PAYPAL_TEST', cast=bool)

SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', cast=bool)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', cast=bool)
SESSION_COOKIE_SAMESITE = env('SESSION_COOKIE_SAMESITE')
CSRF_COOKIE_SAMESITE = env('CSRF_COOKIE_SAMESITE')

DEFAULT_PAGINATION = 4

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_api.authentication.BearerTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S'
}

ALGOLIA = {
    'APPLICATION_ID': env('APPLICATION_ID'),
    'API_KEY': env('API_KEY'),
    'INDEX_PREFIX': env('INDEX_PREFIX')
}

CORS_URLS_REGEXES = r'^/api/.*'

CORS_ALLOWED_ORIGINS = []

if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        'http://localhost:8000',
        'https://localhost:8000'
    ]
