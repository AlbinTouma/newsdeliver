from collections.abc import Generator, Iterator
import httpx
from newsdeliver.ingestfeed import IngestFeed

class StreamRSS:
    def __init__(self, url: str | list[str], client: httpx.Client, browser: object | None = None):
        self.url = url
        self.client = client
        self.browser = browser

    def ingest_feeds(self) -> Generator[str, None, None]:
          for url in self.url:
              for i in IngestFeed(self.url, browser=self.browser, client=self.client).stream_articles():
                  yield i

    def ingest_feed(self) -> Generator[str, None, None]:
        yield list(self.ingest_feeds(self.url))

if __name__ == "__main__":
        from src.StalkNews.clients import network_client, playwright_browser

        google_rss_url = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=Iran"
        bbc_rss_url = "https://feeds.bbci.co.uk/news/rss.xml"

        with network_client() as client:
            stream = StreamRSS(google_rss_url, client)
                    
