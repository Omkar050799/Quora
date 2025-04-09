import os
from celery import Celery
from django.conf import settings

django_settings = os.getenv("DJANGO_SETTINGS")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"quora.settings.{django_settings}")

app = Celery("quora")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Set the task queue (defaulting to "default" if not set in Django settings)
app.conf.task_default_queue = getattr(settings, "CELERY_TASK_DEFAULT_QUEUE", "default")

# Auto-discover tasks from installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Debugging task
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
