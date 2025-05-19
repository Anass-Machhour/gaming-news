from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import logging
from .config import WebsiteConfig
from .fetch import fetch
from .utils import get_element, get_article_url, get_headline, get_thumbnail
from ..models import Website, Article
from ..database import SessionLocal
import aiohttp
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


async def scrape_website_info(session: aiohttp.ClientSession, website: WebsiteConfig, db: Session) -> int:
    html = await fetch(session, website.url)
    soup = BeautifulSoup(html, "html.parser")

    website_db = db.query(Website).filter_by(url=website.url).first()
    if not website_db:
        favicon_tag = soup.find("link", rel="icon") or soup.find(
            "link", rel="apple-touch-icon")
        
        favicon_url = ""
        if favicon_tag:
            href = favicon_tag.get("href", "")
            if href.startswith("https://"):
                favicon_url = href
            else:
                favicon_url = urljoin(website.url, href)

        website_db = Website(
            url=website.url,
            name=website.name,
            favicon_url=favicon_url,
            created_at=datetime.now(timezone.utc)
        )
        db.add(website_db)
        db.commit()

    return website_db.id


async def scrape_articles(session: aiohttp.ClientSession, website: WebsiteConfig, website_id: int, db: Session):
    html = await fetch(session, website.url)
    soup = BeautifulSoup(html, "html.parser")
    section = get_element(soup, website.section_selector)

    if not section:
        logger.warning(f"No section found for {website.name}")
        return

    articles = section.find_all(
        website.article_selector.tag, class_=website.article_selector.class_)
    for article in articles[:10]:
        article_url = get_article_url(website.url, article)
        if not article_url:
            continue

        if db.query(Article).filter_by(url=article_url).first():
            continue

        article_html = await fetch(session, article_url)
        article_soup = BeautifulSoup(article_html, "html.parser")

        headline = get_headline(article_soup, website.headline_selector)
        thumbnail = get_thumbnail(article_soup, website.thumbnail_selector)

        if not headline or not thumbnail:
            continue

        new_article = Article(
            url=article_url,
            headline=headline,
            thumbnail_url=thumbnail,
            website_id=website_id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_article)


async def scrape_website(website: WebsiteConfig):
    async with aiohttp.ClientSession() as session:
        db = SessionLocal()
        try:
            website_id = await scrape_website_info(session, website, db)
            await scrape_articles(session, website, website_id, db)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.exception(f"Error scraping {website.url}")
        finally:
            db.close()
