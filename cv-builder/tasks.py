# tasks.py
import os
import asyncio
import aiohttp
import aioredis
import hashlib
import logging
from celery_app import celery_app

logger = logging.getLogger(__name__)

# Use uvloop if available for improved asyncio performance
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

def get_cache_key(url: str) -> str:
    return "job:" + hashlib.sha256(url.encode("utf-8")).hexdigest()

async def async_fetch_job_page(session: aiohttp.ClientSession, url: str) -> str:
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (AsyncCVBuilder/1.0)"}
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            if attempt == retries:
                logger.exception(f"Failed to fetch {url} after {retries} attempts")
                raise e
            await asyncio.sleep(0.5 * attempt)
    return ""

async def cached_fetch_job_page(redis_conn, session: aiohttp.ClientSession, url: str) -> str:
    key = get_cache_key(url)
    cached = await redis_conn.get(key, encoding="utf-8")
    if cached:
        logger.info(f"Cache hit for URL: {url}")
        return cached
    logger.info(f"Cache miss for URL: {url}. Fetching content...")
    html = await async_fetch_job_page(session, url)
    await redis_conn.set(key, html, expire=3600)  # Set a 1-hour TTL
    return html

async def _process_job_url(url: str) -> str:
    redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    redis_conn = await aioredis.create_redis_pool(redis_url)
    async with aiohttp.ClientSession() as session:
        result = await cached_fetch_job_page(redis_conn, session, url)
    redis_conn.close()
    await redis_conn.wait_closed()
    return result

@celery_app.task
def process_job_url_task(url: str) -> str:
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(_process_job_url(url))
    return result

def process_job_url_sync(url: str) -> str:
    return asyncio.run(_process_job_url(url))
