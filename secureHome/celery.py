import os
from celery import Celery

# Point to Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secureHome.settings')

# Create Celery app
app = Celery('secureHome')

# Read config from Django settings (anything starting with CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py files in all Django apps
app.autodiscover_tasks()

