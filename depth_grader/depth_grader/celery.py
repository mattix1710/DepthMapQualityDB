# depth_grader/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "depth_grader.settings")
app = Celery("depth_grader")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()