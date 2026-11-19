from xmlrpc import client
from contextlib import contextmanager, asynccontextmanager
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


@asynccontextmanager
async def async_httpx_client():
    async with httpx.AsyncClient() as client:
        yield client


@asynccontextmanager
async def async_playwright_browser():
    
    import os
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("\n The playwright python package is not installed.")
        yield

    browser = None
    async with async_playwright() as p:
        if not os.path.exists(p.chromium.executable_path):
            import time
            print("""\n Chrome driver is missing. \n python -m playwright install chromium -m. \n""")
            choice = input("Want to continue scraping without javascript support? [Y/N]: ")
            if choice == "Y":
                yield
                time.sleep(2)
            elif choice == "N":
                exit()
            
            
            
        try:
            browser = await p.chromium.launch()
            yield browser
        except Exception as e:
            raise
        finally:
            if browser: await browser.close()


