from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .config import Selector
import logging
import re

logger = logging.getLogger(__name__)

def get_element(soup: BeautifulSoup, selector: Selector):
    return soup.find(selector.tag, class_=re.compile(rf"^{selector.class_}"))

def get_article_url(base_url: str, article) -> str:
    try:
        link_tag = article.find("a")
        href = link_tag.get("href")
        return urljoin(base_url, href)
    except Exception as e:
        logger.error(f"Error extracting article URL: {e}")
        return ""

def get_headline(soup: BeautifulSoup, selector: str) -> str:
    try:
        headline_tag = soup.find(selector)
        return headline_tag.get_text(strip=True) if headline_tag else ""
    except Exception as e:
        logger.error(f"Error extracting headline: {e}")
        return ""

def get_thumbnail(soup: BeautifulSoup, selector: Selector) -> str:
    try:
        thumb_section = get_element(soup, selector)
        img_tag = thumb_section.find("img") if thumb_section else None
        return img_tag.get("data-src") or img_tag.get("src") if img_tag else ""
    except Exception as e:
        logger.error(f"Error extracting thumbnail: {e}")
        return ""
