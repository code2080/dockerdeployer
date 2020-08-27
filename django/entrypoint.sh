#!/bin/bash
python /script/init_database.py
python manage.py shell < /script/check_connection.py
python manage.py collectstatic --noinput
python manage.py migrate --no-input
python manage.py shell < /script/create_django_admin_user.py 
exec "$@"
