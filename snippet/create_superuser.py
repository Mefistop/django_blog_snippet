import os
from django.contrib.auth import get_user_model

def create_superuser():
    """Create superuser"""
    User = get_user_model()
    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')

    if not User.objects.filter(username=username).exists():
        print("Creating superuser...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully.")
    else:
        print("Superuser already exists.")

if __name__ == "__main__":
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snippet.settings')
    django.setup()
    create_superuser()