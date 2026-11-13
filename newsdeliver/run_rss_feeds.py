from .scraper import orchestrate_rss_workers, orchestrate_article_workers
from queue import Queue
from threading import Thread
from .scraper import scrape_article_async, rss_worker_async
import asyncio
import httpx
from playwright.async_api import async_playwright
from dataclasses import dataclass

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
    c = 0
    while True:
        url = await queue.get()
        try:
            result = await scrape_article_async(client, browser, url)
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

    async with httpx.AsyncClient() as client, async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
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

if __name__=="__main__":
    import httpx

    feed_urls = [

        "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=Iran",
        #"https://feeds.skynews.com/feeds/rss/uk.xml",
        #"https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        #"https://feeds.bbci.co.uk/news/rss.xml"
        #"https://www.gloucestershirelive.co.uk/?service=rss",
        "https://www.cambridge-news.co.uk/?service=rss"
    ]

    asyncio.run(main(feed_urls))
