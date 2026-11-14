from collections.abc import Generator, Iterator
import httpx
from newsdeliver.scraper.ingestfeed import IngestFeed
import threading
from concurrent.futures import ThreadPoolExecutor


class StreamRSS:
    def __init__(self, feed_urls: list[str], client: httpx.Client, browser: object | None = None):
        self.feed_urls = feed_urls
        self.client =client
        self.browser = browser

    def ingest_feeds(self) -> Generator[str, None, None]:
        streams = (IngestFeed(u, browser=self.browser, client=self.client) for u in self.feed_urls)
        for stream in streams:
            for i in stream.stream_articles():
                yield i

    def ingest_feed(self) -> Generator[str, None, None]:
        yield list(self.ingest_feeds(self.feed_urls))


                  
