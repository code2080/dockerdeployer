from django.contrib.auth.models import User
import os

if not User.objects.filter(username=os.environ.get('DJANGO_ADMIN_USERNAME')):
    User.objects.create_superuser(
        os.environ.get('DJANGO_ADMIN_USERNAME'),
        os.environ.get('DJANGO_ADMIN_EMAIL'),
        os.environ.get('DJANGO_ADMIN_PASSWORD'),
    )
    print('Admin user was created.')
else:
    print('Admin user is existed.')