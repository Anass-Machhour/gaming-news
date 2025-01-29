# Web scraping logic
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs
from .database import SessionLocal
from .models import Website, Article
import asyncio


def scrape_webiste(website_data):
    # Create a database session
    db = SessionLocal()

    try:
        response = requests.get(website_data["url"])
        soup = bs(response.text, "html.parser")

        # Get the website's favicon URL form the <link> tag
        favicon_tag = soup.find("link", rel="icon")
        if not favicon_tag:
            favicon_tag = soup.find("link", rel="shortcut icon")

        favicon_url = favicon_tag["href"] if favicon_tag else "No favicon found"

        website = db.query(Website).filter_by(url=website_data["url"]).first()
        if not website:
            # Create a new website entry
            website = Website(
                url=website_data["url"],
                name=website_data["name"],
                favicon_url=favicon_url,
                created_at=datetime.now(timezone.utc)
            )
            db.add(website)
            db.commit()

        # Select the articles section
        section_tag, section_class = website_data["section_selector"][
            "tag"], website_data["section_selector"]["class"]
        main_section = soup.find(
            section_tag,
            class_=section_class
        )

        # Check if the section exist
        if main_section:
            # Select the articles URL
            article_tag, article_class = website_data["article_selector"][
                "tag"], website_data["article_selector"]["class"]
            articles = soup.find_all(article_tag, article_class)
            # Check if articles is not empty
            if articles:
                for article in articles:
                    # Get the article full URL, from href tag and join it with website URL
                    get_href = article.find("a")
                    link = get_href["href"]
                    article_url = urljoin(website_data["url"], link)

                    # Redirecting to the article page
                    response = requests.get(article_url)
                    soup = bs(response.text, "html.parser")

                    # Get the headline
                    headline_tag = soup.find("h1")
                    headline = headline_tag.text.strip()

                    # Select the thumbnail tag
                    thumbnail_selector = soup.find(
                        website_data["thumbnail_selector"]["tag"], website_data["thumbnail_selector"]["class"])
                    thumbnail_tag = thumbnail_selector.find("img")
                    # extract the thumbnail URL
                    thumbnail = thumbnail_tag.get(
                        "data-src", thumbnail_tag.get("src", "No thumbnail"))

                    # Check if the article already exists in database
                    if not db.query(Article).filter_by(url=article_url).first():
                        article_db = Article(
                            url=article_url,
                            headline=headline,
                            thumbnail_url=thumbnail,
                            website_id=website.id,
                            created_at=datetime.now(timezone.utc)
                        )
                        db.add(article_db)

        # Commit all changes to the database
        db.commit()

    except Exception as e:
        # In case of an error will Rollback
        db.rollback()
        print(f"An error occurred: {e}")

    finally:
        db.close()


websites = [
    {
        "name": "engadget",
        "url": "https://www.engadget.com/gaming/pc/",
        "section_selector": {"tag": "ul", "class": "D(b) Jc(sb) Flw(w) M(0) P(0) List(n)"},
        "article_selector": {"tag": "li", "class": "Mb(24px) Bxz(bb)"},
        "headline_selector": "h1",
        "thumbnail_selector": {"tag": "div", "class": "caas-img-container"},
    },
    {
        "name": "kotaku",
        "url": "https://kotaku.com/latest",
        "section_selector": {"tag": "div", "class": "sc-17uq8ex-0 fakHlO"},
        "article_selector": {"tag": "div", "class": "sc-3kpz0l-2 ciHPAq"},
        "headline_selector": "h1",
        "thumbnail_selector": {"tag": "div", "class": "sc-1eow4w5-3 hGpdBg"},
    }
]


def main():
    for website in websites:
        scrape_webiste(website)
    print("Scrapped")


if __name__ == "__main__":
    main()
