# celery_app.py
import os
from celery import Celery

broker_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("cv_builder_tasks", broker=broker_url, backend=broker_url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
