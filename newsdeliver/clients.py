from xmlrpc import client
from contextlib import contextmanager
import httpx


@contextmanager
def network_client(proxy: str | None = None, timeout: float | None = 10.0, user_agent: str | None = None):
    headers = {"User-Agent": user_agent} if user_agent else None
    with httpx.Client(proxy=proxy, timeout=timeout, headers=headers) as client:
        try:
            yield client
        finally:
            client.close()

@contextmanager
def playwright_browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
            yield browser
        except Exception as e:
            raise Exception(e)
        finally:
            browser.close()


