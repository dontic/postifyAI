from bs4 import BeautifulSoup
import requests

from logging_setup import setup_logger

log = setup_logger(__name__)


def fetch_content(url: str) -> str:
    # Fetch content from the URL
    try:
        log.info(f"Fetching content from {url}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find("body")

        if body:
            content_body = body.get_text(separator="\n", strip=True)
        else:
            content_body = ""
    except Exception as e:
        log.warning(f"Failed to fetch content from {url}: {e}")
        content_body = ""

    return content_body


def fetch_all_contents(urls: list[str]) -> tuple[list[str], str | None]:
    log.info(f"Fetching content from {len(urls)} URLs...")

    # Fetch content from multiple URLs
    contents = [fetch_content(url) for url in urls]

    # Remove empty contents
    contents = [content for content in contents if content]

    log.info(f"Fetched {len(contents)} contents")

    if not contents:
        log.error("No content could be fetched from the URLs")
        return [], "No content could be fetched from the URLs"

    return contents, None
