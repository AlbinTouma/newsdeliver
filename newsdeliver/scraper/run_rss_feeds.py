from queue import Queue
from dataclasses import dataclass
from threading import Thread
from .async_page import scrape_article_async
from .async_rss_feed import rss_worker_async
import asyncio
import httpx
from playwright.async_api import async_playwright
from newsdeliver.scraper.clients import async_httpx_client, async_playwright_browser



@dataclass 
class Counter:
    npages: int

    def increment(self):
        self.npages += 1


async def feed_producer(client, feed, queue):
    feed_urls: list[str] = await rss_worker_async(client, feed)
    if len(feed_urls) <0:
        return

    for url in feed_urls:
        await queue.put(url)

async def article_consumer(client, browser, queue, counter):
    while True:
        url = await queue.get()
        try:
            result = await scrape_article_async(client, browser, url)
            print(result)
            if isinstance(result, Exception):
                raise Exception(result)
            
            counter.increment()
            
            
        except Exception as e:
            print(e)
        finally:
            queue.task_done()


async def main(feed_urls, num_workers=4):
    queue = asyncio.Queue()
    counter = Counter(0)

    async with (async_httpx_client() as client, async_playwright_browser() as browser): 
        context = None
        if browser:
            context = await browser.new_context()
        try:
            workers = [
                asyncio.create_task(article_consumer(client, context, queue, counter))
                for _ in range(num_workers)
                ]

            await asyncio.gather(*(feed_producer(client, feed, queue) for feed in feed_urls))
            await queue.join()
            for w in workers:
                w.cancel()

            print(counter.npages)
        finally:
            await browser.close()


