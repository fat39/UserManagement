"""
Django settings for UserManagement project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k3bs)k-zhc35puu&n2iq@b*5-qcq15!1fn6ui5c&4($zsii5ip'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'rbac.apps.RbacConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "rbac.middleware.rbac.RbacMiddleware",
]

ROOT_URLCONF = 'UserManagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'UserManagement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"static"),
)


# ############################## RBAC权限相关配置开始 ##############################
# # 无需权限控制的URL
RBAC_NO_AUTH_URL = [
    '^/$',
    '/Login.html',
    "/Logout/",
    # '/index.html',
    '/Register.html',
    '/admin.*',
    '/rbac.*',
    "/check_code/",
]

# session中保存权限信息的Key
RBAC_PERMISSION_SESSION_KEY = "rbac_permission_session_key"

# Http请求中传入的参数，根据其获取GET、POST、EDIT等检测用户是否具有相应权限
# 例如：
#       http://www.example.com?md=get   表示获取
#       http://www.example.com?md=post  表示添加
#       http://www.example.com?md=del   表示删除
RBAC_QUERY_KEY = "md"
RBAC_DEFAULT_QUERY_VALUE = "get"

# 无权访问时，页面提示信息
RBAC_PERMISSION_MSG = "无权限访问"

# Session中保存菜单和权限信息的Key
RBAC_MENU_PERMISSION_SESSION_KEY = "rbac_menu_permission_session_key"
RBAC_MENU_KEY = "rbac_menu_key"
RBAC_MENU_PERMISSION_KEY = "rbac_menu_permission_key"

# 菜单主题
RBAC_THEME = "default"
# ############################## RBAC权限相关配置结束 ##############################



'''
    初始化权限，获取当前用户权限并添加到session中
    将当前用户权限信息转换为以下格式，并将其添加到Session中
        {
            '/index.html': ['GET','POST','DEL','EDIT],
            '/detail-(\d+).html': ['GET','POST','DEL','EDIT],
        }
    
{
    'rbac_menu_key': 
        [
            {'id': 1, 'caption': '菜单1', 'parent_id': None}, 
            {'id': 2, 'caption': '菜单2', 'parent_id': None}
        ],
    'rbac_menu_permission_key': 
        [
            {'permission_id': 1, 'permission__url': '/Group.html', 'permission__caption': '用户组管理', 'permission__menu_id': 2}, 
            {'permission_id': 2, 'permission__url': '/User.html', 'permission__caption': '用户管理', 'permission__menu_id': 1}
        ]
}

{
    '/Group.html': ['GET', 'POST'],
    '/User.html': ['POST', 'GET']
}

'''
