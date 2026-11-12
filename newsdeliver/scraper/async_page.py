import httpx
from trafilatura import extract
import json
from playwright.async_api  import async_playwright
import asyncio

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
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        return await page.content()
    except Exception as e:
        raise Exception("Failed to fetch with browser", e)
        return None
    finally:
        if page is not None:
            page.close()

async def fetch_article(url, client, browser) -> str | httpx._exceptions.HTTPError:
    """Fetches the article content from the given URL using either httpx or Playwright.
    If the httpx request fails, it will attempt to fetch the content using Playwright unless Playwright is unavailable."""
    response = None
    try:
        response = await client.get(url)
        match response.status_code:
            case 200:
                return response.text
            case status if 200 < status < 400 and browser is not None:
                html_content = await fetch_with_browser(url, browser)
                return html_content
            case None:
                raise ValueError("Response is None.")
            case _:
                raise httpx._exceptions.HTTPError(f"X --{response.status_code} {url}")
    except Exception as e:
        return e


def parse_article(html_content: str) -> str | None:
        """
        Parses the HTML content of an article and returns the extracted text in JSON format.
        params:
            html_content: str - The HTML content of the article
        returns:
            str - The extracted text in JSON format
        """
        if html_content is None:
            return None

        parsed_html = extract(html_content, output_format="json", with_metadata=True)
        if parsed_html is None:
            raise ValueError(f"Parsed HTML failed for \n {parsed_html}")
            
        return json.loads(parsed_html)


async def scrape_article_async(client, browser, url: str) -> dict[str] | Exception:
    """Scrape individual article url"""
    try:
        html_content = await fetch_article(url, client, browser)
        if isinstance(html_content, Exception):
            raise html_content

        if html_content:
            parsed_article = await asyncio.to_thread(parse_article, html_content)
            return parsed_article
        else:
            return None
    except Exception as e:
        return e
