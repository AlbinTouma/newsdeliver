from operator import contains
from newsdeliver.utils import decode_rss_links, parse_rss_feed, parse_article, fetch_article 
import httpx
from collections.abc import Generator, Iterator
from concurrent.futures import ThreadPoolExecutor



class IngestFeed():

    def __init__(
            self,
            url: str,
            client: httpx.Client | None = None,
            browser: object | None = None
            ):

            self.rss_url = url
            self.browser = browser 
            self.client = client


    def scrape_article(self, url):
        if "news.google.com/rss" in url:
            url = decode_rss_links(url)

        article = fetch_article(url, self.client, self.browser)
        if not article:
            return

        content_json = parse_article(article)
        return content_json

    def stream_articles(self) -> Generator[str, None, None]:
        try:
            response = self.client.get(self.rss_url)
            rss_feed = parse_rss_feed(response)

            with ThreadPoolExecutor(max_workers=4) as executor:
                results = executor.map(self.scrape_article, rss_feed)
                for result in results:
                    yield result

        except Exception as e:
            print(f'Error at self.rss_url: {e}')

    def fetch_all(self) -> list[str]:
        return list(self.stream_articles())



if __name__ =="__main__":

    google_rss_url ="https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=Iran"
    bbc_rss_url = "https://feeds.bbci.co.uk/news/rss.xml"
    guardian = "https://www.theguardian.com/europe/rss" 


    rss = IngestFeed(google_rss_url, httpx.Client())
    for i in rss.stream_articles():
        print(i)
