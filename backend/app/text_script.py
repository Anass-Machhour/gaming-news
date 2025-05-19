import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re

websites = [
    {
        "name": "kotaku",
        "url": "https://kotaku.com/culture/news",
        "section_selector": {"tag": "div", "class": "sc-17uq8ex-0 fakHlO"},
        "article_selector": {"tag": "div", "class": "sc-cw4lnv-12 kQoJyO"},
        "headline_selector": "h1",
        "thumbnail_selector": {"tag": "div", "class": "sc-1eow4w5-3 hGpdBg"},
    },
    # {
    #     "name": "engadget",
    #     "url": "https://www.engadget.com/gaming/pc/",
    #     "section_selector": {"tag": "div", "class": "! mt-0 flex items-start justify-between"},
    #     "article_selector": {"tag": "li", "class": "mb-6 box-border"},
    #     "headline_selector": "h1",
    #     "thumbnail_selector": {"tag": "div", "class": "caas-img-container"},
    # },
    # {
    #     "name": "pcgamer",
    #     "url": "https://www.pcgamer.com/games/",
    #     "section_selector": {"tag": "div", "class": "clear-both widget widget-dynamic widget-latest-top widget-dynamic-latest-top widget-dynamic-listv2 wdn-listv2-layout-sm-scroll wdn-listv2-layout-md-scroll flexi-carouzelize"},
    #     "article_selector": {"tag": "li", "class": "wdn-listv2-item item-slot- item-slot-color-"},
    #     "headline_selector": "h1",
    #     "thumbnail_selector": {"tag": "div", "class": "clear-both widget widget-contentparsed widget-content widget-contentparsed-content widget-content-parsed widget-content-parsed-content_document"},
    # },
    # {
    #     "name": "polygon",
    #     "url": "https://www.polygon.com/pc",
    #     "section_selector": {"tag": "div", "class": "v7zk5q3"},
    #     "article_selector": {"tag": "div", "class": "duet--content-cards--content-card _15ic40z3 _15ic40z0 cmuha60"},
    #     "headline_selector": "h1",
    #     "thumbnail_selector": {"tag": "div", "class": "duet--layout--entry-body _4ljyn30"},
    # },
]


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def test_website_live(website):
    print(f"\n== Testing: {website['name']} ==")
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, website["url"])
        soup = bs(html, "html.parser")

        # Find article section
        section = soup.find_all(
            website["section_selector"]["tag"], class_=re.compile(rf"^{website["section_selector"]["class"]}"))
        if not section:
            print("❌ Section not found")
            return

        # Find articles
        articles = soup.find_all(
            website["article_selector"]["tag"], class_=re.compile(rf"^{website["article_selector"]["class"]}"))

        if not articles:
            print("❌ No articles found")
            return

        print(f"✅ Found {len(articles)} articles")
        for article in articles[:3]:  # Just sample 3
            try:
                href = article.find("a")["href"]
                article_url = urljoin(website["url"], href)

                # Select the thumbnail tag
                html = await fetch(session, article_url)
                soup = bs(html, "html.parser")
                thumbnail_selector = soup.find(
                    website["thumbnail_selector"]["tag"], website["thumbnail_selector"]["class"])
                # extract the thumbnail URL
                thumbnail_tag = thumbnail_selector.find("img")
                thumbnail = thumbnail_tag.get(
                    "data-src", thumbnail_tag.get("src", "No thumbnail"))

                print(f"- URL: {article_url}")
                print(f"- THUMBNAIL_URL: {thumbnail}")
            except Exception as e:
                print(f"⚠️ Error extracting URL: URL: {article_url}\n {e}")


async def main():
    await asyncio.gather(*(test_website_live(w) for w in websites))

if __name__ == "__main__":
    asyncio.run(main())
