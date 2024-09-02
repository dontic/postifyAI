from bs4 import BeautifulSoup
import requests


def fetch_content(url):
    # Fetch content from the URL
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find("body")

        if body:
            content_body = body.get_text(separator="\n", strip=True)
        else:
            content_body = ""
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        content_body = ""

    return content_body


def fetch_all_contents(urls):
    # Fetch content from multiple URLs
    contents = [fetch_content(url) for url in urls]

    # Remove empty contents
    contents = [content for content in contents if content]

    return contents
