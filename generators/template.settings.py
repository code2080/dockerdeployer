SECRET_KEY = '{{ secret_key }}'
DEBUG = {{ debug }}
ALLOWED_HOSTS = ['*', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ db_name }}',
        'USER': '{{ db_usr }}',
        'PASSWORD': '{{ db_pwd }}',
        'HOST': 'database',
    }
}

STATIC_URL = '{{ static_url }}'
MEDIA_URL = '{{ media_url }}'
STATIC_ROOT = '{{ static_root }}'
MEDIA_ROOT = '{{ media_root }}'