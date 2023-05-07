import os
import environ 

from pathlib import Path


#Environnement
env=environ.Env()

environ.Env.read_env()
#

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ldd%@#bd&cy@=47@+48u1lkz&ka+lil#7o)x)ku_g!j#!f13)1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app']

# Email
EMAIL_BACKEND= 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL="abdouanjouanais@gmail.com"
NOTIFY_EMAIL="abdouanjouanais@gmail.com"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crispy_forms',
    'cart',
    'utilisateurs'
]

AUTH_USER_MODEL = 'utilisateurs.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AbdallahMarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'django.template.backends.jinja2.Jinja2'
            ],
        },
    },
]

WSGI_APPLICATION = 'AbdallahMarket.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR =True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

#Fichiers static
STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,"static")]
#STATIC_ROOT=os.path.join(BASE_DIR,"static_root")

#Les photos disponibilitée
MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,"media")

#
CRISPY_TEMPLATE_PACK='bootstrap4'

#PayPal
PAYPAL_CLIENT_ID=env('PAYPAL_SANDBOX_CLIENT_ID')
PAYPAL_SECRET_KEY=env('PAYPAL_SANDBOX_SECRET_KEY')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

''' if DEBUG is False:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT=True
    SESSION_COOKIE_SECURE=True 
    CSRF_COOKIE_SECURE=True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_BROWSER_XSS_FILTER=True
    SECURE_REDIRECT_EXEMPT=[]
    SECURE_HSTS_INCLUDE_SUBDOMAINS=True
    
    ALLOWED_HOSTS=['https://datadosis.com']
    
    EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
    
    DATABASES={
        'default': {
        'ENGINE': 'django.db.backends.psg_ecom1',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
    }
    PAYPAL_CLIENT_ID=env('PAYPAL_LIVE_CLIENT_ID')
    PAYPAL_SECRET_KEY=env('PAYPAL_LIVE_SECRET_KEY') '''

#Pour la redirection sur les vues fondées 
LOGIN_URL="/auth"