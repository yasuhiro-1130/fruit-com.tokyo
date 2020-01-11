#!/bin/sh  

if [ "$DATABASE" = "postgres" ]  
then  
    echo "Waiting for postgres..."  

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do  
      sleep 0.1  
    done  

    echo "PostgreSQL started"  
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear

EXIST_ADMIN=`python manage.py shell < /usr/src/fruits/check_admin.py`
if [ ${EXIST_ADMIN} = 'True' ]; then
  echo "admin user already exists!":
else
echo "Does not exist admin user."
python manage.py shell -c "\
from django.contrib.auth import get_user_model;\
import os;\
User = get_user_model();\
User.objects.create_superuser(os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD'));\
"
echo "Created admin user!!"
fi
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application \
"$@"  