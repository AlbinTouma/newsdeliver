from .scraper import orchestrate_rss_workers, orchestrate_article_workers
from queue import Queue
from threading import Thread
from .scraper import scrape_article_async, rss_worker_async
import asyncio
import httpx



async def main(feed_urls):
    async with httpx.AsyncClient() as client:
        urls = await rss_worker_async(client, feed_urls)

        if urls is None:
            exit()

        for url in urls:
            page = await scrape_article_async(client, None, url)
            print(page)


if __name__=="__main__":
    import httpx

    feed_urls = [

        #"https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=Iran",
        "https://feeds.skynews.com/feeds/rss/uk.xml",
        #"https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://feeds.bbci.co.uk/news/rss.xml"
    ]

    asyncio.run(main("https://feeds.bbci.co.uk/news/rss.xml"))
