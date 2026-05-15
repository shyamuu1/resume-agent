"""Scraper Module"""

import urllib
from utils.llm_utils import get_Logger

logger = get_Logger("ScraperNode")

def scrape_job_description(url: str) -> str:
    """
    Uses Jina Reader to scrape a job posting URL
    and return clean markdown text.
    """
    jina_url = f"https://r.jina.ai/{url}"

    request = urllib.request.Request(jina_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
    except Exception as e:
        logger.error(f"Error fetching job description: {e}")
        return ""