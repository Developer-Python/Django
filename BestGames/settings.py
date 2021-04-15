# Модули для работы с [OS]
import os, sys, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Изменнёная директория для пойска приложений
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Использовать режим отладки ?
DEBUG = True

# Защита подписанных данных
SECRET_KEY = 'd*ztfilbtuw5jr934&(xcj-%%!7&lk2ju%3!3pp!cno+n1ftef'

# Разрешённые хосты для которых может работать текущий сайт
ALLOWED_HOSTS = ['*']

# Список установленных приложений
INSTALLED_APPS = [

    # Стандартные приложения
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Мой приложения
    'main.apps.MainConfig',
    'accounts.apps.AccountsConfig',
    'sberbank.apps.AppConfig',
]


# Промежуточный слой
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Главня конфигурация ссылок
ROOT_URLCONF = 'BestGames.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Использование шаблонов из папки [templates]
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.categories_and_cart',
            ],
        },
    },
]

# Выступает в роли простого сервера [WSGI]
WSGI_APPLICATION = 'BestGames.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Управления пользовательскими паролями.
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

# Язык
LANGUAGE_CODE = 'ru'

# Часовой пояс
TIME_ZONE = 'UTC'

# Использовать механизм перевода [Django] ?
USE_I18N = True

# Использовать локализованный формат даты ?
USE_L10N = True

# Использовать часовой пояс ?
USE_TZ = True

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
