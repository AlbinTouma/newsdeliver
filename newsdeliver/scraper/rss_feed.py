# First step is a worker that parses RSS feeds spits out urls for a worker to schedule.
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
import feedparser
import httpx
from collections.abc import Generator
from googlenewsdecoder import gnewsdecoder

def get_feed(client, url):
    """Make a httpx call to rss feed and return response.content"""
    try:
        response = client.get(url)
        return response.content
    except Exception as e:
        print(e)


def parse_rss_feed(response) -> list[str]:
        """
                Parses the RSS feed and returns the links of the articles.
                params:
                    response: httpx.Response - The response object from the RSS feed request
                returns:
                    list[str] - A list of links for each article in the RSS feed
        """
        try:
            feed= feedparser.parse(BytesIO(response.content))
            return [item['link'] for item in feed['entries']]
        except Exception as e:
            raise Exception("Error", e)


def stream_parse_rss_feed(response) -> Generator[str, None, None]:
        """
                Parses the RSS feed and yields the links of the articles.
                params:
                    response: httpx.Response - The response object from the RSS feed request
                yields:
                    str - The link of each article in the RSS feed
        """
        try:
            feed= feedparser.parse(BytesIO(response.content))
            for item in feed['entries']:
                yield item['link']
        except Exception as e:
            raise Exception("Error", e)


def decode_rss_links(url) -> str:
        """Decodes urls from Google RSS feed. Returns decoded url if successful, otherwise returns the original url.
        params:
            url: str - The url to decode
        returns:
            str - The decoded url or the original url if decoding fails
        """
        decoded = gnewsdecoder(url)
        if decoded['decoded_url']:
            return decoded['decoded_url']

        return url



def rss_worker(client, url: str) -> list[str] | None:
    """Worker fetches and parses an rss feed, and returns article urls.
    params:
        url: str - The url of the rss feed
    returns:
        list[str] - A list of links for each article in the RSS feed
    """
    try:
        response = client.get(url)
        rss_feed = parse_rss_feed(response)
        
        if url.startswith("https://news.google.com/rss"):
            gnews_results: list[dict] = [gnewsdecoder(url) for url in rss_feed]
            decoded_urls: list[sr] = [i['decoded_url'] for i in gnews_results if i["status"] == True]
            return decoded_urls


        return rss_feed
    
    except Exception as e:
        print(f'Error at {url}: {e}')




