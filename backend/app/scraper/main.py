import asyncio
import logging
from .config import websites
from .website_scraper import scrape_website
from .cleanup import delete_old_articles

logging.basicConfig(level=logging.INFO)

async def start_scraping():
    tasks = [scrape_website(site) for site in websites]
    await asyncio.gather(*tasks)
    delete_old_articles()
    logging.info("====== Scraping finished ======")

if __name__ == "__main__":
    asyncio.run(start_scraping())