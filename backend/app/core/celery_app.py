import os
from celery import Celery

# Use a local Redis server. In production, this would come from an environment variable.
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "autohire_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.workers.scraper_tasks", "app.workers.apply_tasks", "app.workers.email_monitor"]
)

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Set up periodic tasks if necessary (e.g., polling email every 15 minutes)
celery_app.conf.beat_schedule = {
    'check-emails-every-15-minutes': {
        'task': 'app.workers.email_monitor.poll_recruiter_emails',
        'schedule': 900.0, # 15 minutes
    },
}
