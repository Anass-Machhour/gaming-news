import aiohttp
from bs4 import BeautifulSoup as bs
from datetime import datetime, timezone
from urllib.parse import urljoin
from .models import Website, Article


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_website(website_data, db):
    try:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, website_data["url"])
            soup = bs(html, "html.parser")

            # Get the website's favicon URL form the <link> tag
            favicon_tag = soup.find("link", rel="icon")
            if not favicon_tag:
                favicon_tag = soup.find("link", rel="apple-touch-icon")

            favicon_url = favicon_tag["href"] if favicon_tag else "No favicon found"

            website = db.query(Website).filter_by(
                url=website_data["url"]).first()

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

            await scrape_articles(website_data, website.id, session, db)

    except Exception as e:
        # In case of an error will Rollback
        db.rollback()
        print(f"An error occurred scraping {website_data["url"]}: {e}")


async def scrape_articles(website_data, websiteID, session, db):
    try:
        html = await fetch(session, website_data["url"])
        soup = bs(html, "html.parser")

        # Select the articles section
        section_tag, section_class = website_data["section_selector"][
            "tag"], website_data["section_selector"]["class"]

        main_section = soup.find(section_tag, class_=section_class)

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
                    html = await fetch(session, article_url)
                    soup = bs(html, "html.parser")

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
                            website_id=websiteID,
                            created_at=datetime.now(timezone.utc)
                        )
                        db.add(article_db)
            else:
                print("Articles not found")
        else:
            print("Section not found")

    # In case of an error will Rollback
    except Exception as e:
        db.rollback()
        print(f"error occurred scraping articles from {
              website_data["url"]}: {e}")
