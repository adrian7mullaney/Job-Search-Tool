# app.py
import os
import redis
import asyncio
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request, jsonify, send_from_directory
from celery.result import AsyncResult
from tasks import process_job_url_task, process_job_url_sync

# Initialize Sentry for error tracking (optional: set SENTRY_DSN environment variable)
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='cv-builder-frontend/build')

# Connect to Redis
redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
redis_conn = redis.from_url(redis_url)

# API Endpoint for synchronous processing (for testing)
@app.route("/api/process", methods=["POST"])
def process():
    data = request.get_json() or {}
    url = data.get("url")
    if not url:
        logger.error("No URL provided in /api/process request.")
        return jsonify({"error": "Missing URL"}), 400
    try:
        html_content = process_job_url_sync(url)
        snippet = html_content[:200] + "..." if len(html_content) > 200 else html_content
        return jsonify({"url": url, "content_snippet": snippet})
    except Exception as e:
        logger.exception(f"Error processing URL synchronously: {url}")
        return jsonify({"error": str(e)}), 500

# API Endpoint to offload processing to Celery task
@app.route("/api/async-process", methods=["POST"])
def async_process():
    data = request.get_json() or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    task = process_job_url_task.delay(url)
    return jsonify({"task_id": task.id, "status": "Processing"}), 202

# Endpoint to check status of a Celery task
@app.route("/api/task-status/<task_id>", methods=["GET"])
def task_status(task_id):
    result = AsyncResult(task_id)
    return jsonify({
        "task_id": task_id,
        "state": result.state,
        "result": result.result if result.ready() else None
    })

# Serve React static files for all non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
