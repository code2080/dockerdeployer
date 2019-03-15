DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ db_name }}',
        'USER': '{{ db_usr }}',
        'PASSWORD': '{{ db_pwd }}',
        'HOST': 'database',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/django/static/'
MEDIA_ROOT = '/django/media/'

{% for setting in settings %}
{{ setting.key }} = {{ setting.value|tojson }}
{% endfor %}