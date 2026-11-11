import httpx
from trafilatura import extract
import json
playwright.async_api import async_playwright

async def fetch_with_browser(url, browser) -> str | None:
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

async def fetch_article(url, client, browser) -> str | None:
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

        parsed_html = extract(html_content, output_format="json", with_metadata=True)
        return json.loads(parsed_html)


async def scrape_article(url: str) -> None:
    """Scrape individual article url"""
    try:
        html_content = await fetch_article(url, client, browser)
        if html_content:
            parsed_article = await asyncio.to_thread(parse_article, "https://example.com")
            return parsed_article
        else:
            return None
    except Exception as e:
        print(e)
        raise

