import aiohttp
from bs4 import BeautifulSoup as bs
from datetime import datetime, timezone
import re
from urllib.parse import urljoin
from .models import Website, Article


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_website(website, db):
    try:
        async with aiohttp.ClientSession() as session:

            website_id = await scrape_website_info(session, website, db)

            await scrape_articles(website, website_id, session, db)

    except Exception as e:
        # In case of an error will Rollback
        db.rollback()
        print(f"An error occurred scraping {website["url"]}: {e}")


async def scrape_articles(website, websiteID, session, db):
    try:
        html = await fetch(session, website["url"])
        soup = bs(html, "html.parser")

        # Select the articles section
        section_tag, section_class = website["section_selector"][
            "tag"], website["section_selector"]["class"]

        main_section = soup.find(section_tag, class_=section_class)

        # Check if the section exist
        if main_section:
            # Select the articles URL
            article_tag, article_class = website["article_selector"][
                "tag"], website["article_selector"]["class"]

            articles = soup.find_all(
                article_tag, class_=re.compile(rf"^{article_class}"))

            # Check if articles is not empty
            if articles:
                for article in articles[:10]:
                    article_url = scrape_article_url(website, article)
                    
                    if type(article_url) == TypeError:
                        print(article_url)
                        continue

                    article_db = db.query(Article).filter_by(
                        url=article_url).first()

                    # If the article doesn't exist in database, add it
                    if not article_db:
                        # Redirecting to the article page
                        html = await fetch(session, article_url)
                        soup = bs(html, "html.parser")

                        headline = scrape_headline(article_url, soup)

                        thumbnail = scrape_thumbnail(
                            website, article_url, soup)
                        
                        if not thumbnail or not headline:
                            continue

                        # After collecting all the data, store the article into the database
                        article_db = Article(
                            url=article_url,
                            headline=headline,
                            thumbnail_url=thumbnail,
                            website_id=websiteID,
                            created_at=datetime.now(timezone.utc)
                        )
                        db.add(article_db)

                # Commit after iterating over the articles
                db.commit()

            else:
                print("Articles not found")
        else:
            print("Section not found")

    # In case of an error will Rollback
    except Exception as e:
        db.rollback()
        print(f'error occurred scraping articles from {website["url"]}: {e}')


async def scrape_website_info(session, website, db):
    try:
        html = await fetch(session, website["url"])
        soup = bs(html, "html.parser")
        website_db = db.query(Website).filter_by(
            url=website["url"]).first()

        if not website_db:
            # Get the website's favicon URL form the <link> tag
            favicon_tag = soup.find("link", rel="icon")
            if not favicon_tag:
                favicon_tag = soup.find("link", rel="apple-touch-icon")

            favicon_url = favicon_tag["href"] if favicon_tag else "No favicon found"
            # Create a new website entry
            website_db = Website(
                url=website["url"],
                name=website["name"],
                favicon_url=favicon_url,
                created_at=datetime.now(timezone.utc)
            )
            db.add(website_db)
            db.commit()

        return website_db.id

    except Exception as e:
        # In case of an error will Rollback
        db.rollback()
        print(f"An error occurred scraping {e}")


def scrape_article_url(website, article):
    # Get the article full URL, from href tag and join it with website URL
    try:
        get_href = article.find("a")
        link = get_href["href"]
        article_url = urljoin(website["url"], link)

        return article_url

    except Exception as e:
        print(f'An error occurred scraping URL for {article}: {e}')
        return e


def scrape_headline(article, soup):
    # Get the headline
    try:
        headline_tag = soup.find("h1")
        headline = headline_tag.text.strip()

        return headline

    except Exception as e:
        print(f'An error occurred scraping headline for {article}: {e}')
        return None


def scrape_thumbnail(website, article, soup):
    # Get thumbnail URL
    try:
        # Select the thumbnail tag
        thumbnail_selector = soup.find(
            website["thumbnail_selector"]["tag"], website["thumbnail_selector"]["class"])
        # extract the thumbnail URL
        thumbnail_tag = thumbnail_selector.find("img")
        thumbnail = thumbnail_tag.get(
            "data-src", thumbnail_tag.get("src", "No thumbnail"))

        return thumbnail

    except Exception as e:
        print(f'An error occurred scraping thumbnail for {article}: {e}')
        return None
