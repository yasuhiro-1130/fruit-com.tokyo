from django.contrib.auth import get_user_model
import os

User = get_user_model()

try:
    User.objects.get(email=os.environ.get('ADMIN_EMAIL'))
    print('True')
except User.DoesNotExist:
    print('False')
