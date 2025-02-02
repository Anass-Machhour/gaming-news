import asyncio
import os
from celery import Celery, shared_task
from celery.schedules import crontab
from .database import SessionLocal
from .scraper import scrape_website

# Initialize Celery
app = Celery(
    "scraper_tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

# Configure Celery settings
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Trigger Celery beat tasks every 8 hours
app.conf.beat_schedule = {
    'scrape-every-8hours': {
        'task': 'app.tasks.scrape_website_task',
        'schedule': crontab(minute=0, hour="*/8"),
    },
}


websites = [
    {
        "name": "kotaku",
        "url": "https://kotaku.com/culture/news",
        "section_selector": {"tag": "div", "class": "sc-17uq8ex-0 fakHlO"},
        "article_selector": {"tag": "div", "class": "sc-cw4lnv-12 kQoJyO"},
        "headline_selector": "h1",
        "thumbnail_selector": {"tag": "div", "class": "sc-1eow4w5-3 hGpdBg"},
    },
    {
        "name": "engadget",
        "url": "https://www.engadget.com/gaming/pc/",
        "section_selector": {"tag": "ul", "class": "D(b) Jc(sb) Flw(w) M(0) P(0) List(n)"},
        "article_selector": {"tag": "li", "class": "Mb(24px) Bxz(bb)"},
        "headline_selector": "h1",
        "thumbnail_selector": {"tag": "div", "class": "caas-img-container"},
    },
]


@shared_task
def scrape_website_task():
    db = SessionLocal()
    try:
        for website in websites:
            asyncio.run(scrape_website(website, db))
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error occur {website["url"]}: {e}")
    finally:
        db.close()


scrape_website_task.delay()
