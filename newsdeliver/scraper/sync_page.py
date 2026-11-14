import httpx
from trafilatura import extract
import json
from playwright.sync_api import sync_playwright

def fetch_with_browser(url, browser) -> str | None:
    """Fetches the article content from the given URL using Playwright.
    params:
        url: str - The URL of the article to fetch       
        browser: playwright.sync_api.Browser - The Playwright browser instance
    returns:
        str - The HTML content of the article
    """
    page = None
    try:
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        return page.content()
    except Exception:
        return None
    finally:
        if page is not None:
            page.close()

def fetch_article(url, client, browser) -> str | None:
    """Fetches the article content from the given URL using either httpx or Playwright.
    If the httpx request fails, it will attempt to fetch the content using Playwright unless Playwright is unavailable."""
    response = None
    try:
        response = client.get(url)
        if response.status_code == 200:
            return response.text
        elif browser:
            return fetch_with_browser(url, browser)
        return response 
    except Exception as e:
        print("Exception request", e)
        print(response.status_code)


def parse_article(html_content: str) -> str | None:
        """
        Parses the HTML content of an article and returns the extracted text in JSON format.
        params:
            html_content: str - The HTML content of the article
        returns:
            str - The extracted text in JSON format
        """
        if not html_content:
            return None

        return extract(html_content, output_format="json", with_metadata=True)


def scrape_article_worker(url: str) -> None:
    """Worker fetches and parses an article, and returns the extracted text in JSON format.
    params:
        url: str - The url of the article
    returns:
        None
    """
    try:
        with httpx.Client() as client:
            html_content = fetch_article(url, client, None)
            if html_content:
                parsed_article = parse_article(html_content)
                article = json.loads(parsed_article).get('title')
                return article
            else:
                print(f"Failed to fetch article from {url}")
                return None
    except Exception as e:
        print(f"Error processing article {url}: {e}")
        print(e)

