"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ep!bjl^bjip#c+j$5@(1y%%nj==v5*-gg1)owphh=&-2l!q0=^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'haystack',
    # 'books',
    'blog',
    'comments',
    'myauth',
    # django-allauth需要的
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.github',
]

# SITE_ID = 13  # https://stackoverflow.com/questions/25468676/django-sites-model-what-is-and-why-is-site-id-1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        # 'DIRS': [os.path.join(os.path.dirname(__file__), '../templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                # 'django.template.context_processors.request',
            ],
            'libraries': {
                'blog_tags': 'blog.templatetags.blog_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoDB',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '201919',
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
# 为了把项目中全部静态文件收集到一个目录下
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# HAYSTACK配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 指定搜索引擎
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        # 指定索引文件存放位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
# 对搜索结果分页
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
# 指定什么时候更新索引，这里设置每当有文章更新时就更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# ------------------------------------------认证相关-----------------------------
# 指定自定义用户模型的位置
AUTH_USER_MODEL = 'myauth.User'

# 更改login_required装饰器的默认login_url参数，也可以使用login_required(login_url=)方式
LOGIN_URL = '/login'
# 如果在地址栏输入URL进行登录或者注销，则无法获取next值，在这里设置跳转到首页
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# 模拟发送邮件到终端
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# from mysite.setting_email import *


# 设置使用哪些backends对用户凭据进行验证
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Django内置的backend
)
# -----------------------------------------------------------------------------

from .setting_log import Mylog
LOGGING = Mylog
