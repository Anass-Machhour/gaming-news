import aiohttp
import logging

logger = logging.getLogger(__name__)

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logger.error(f"Fetch failed for {url}: {e}")
        return ""