from .rss_feed import rss_worker
from .page import scrape_article_worker
from concurrent.futures import ThreadPoolExecutor, as_completed


def orchestrate_rss_workers(client, feed_urls: list[str], article_urls_queue) -> None:
    """Creates and orchestrates RSS workers from a list of RSS URLs.
    params:
        feed_urls: list[str] - A list of RSS feed URLs to stream
    returns:
        None    """

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(rss_worker, client, url) for url in feed_urls]
        for future in as_completed(futures):
            try:
                for link in future.result():
                    article_urls_queue.put(link)
            except Exception as e:
                print(f"Error processing feed: {e}")


def orchestrate_article_workers(article_urls_queue) -> None:
    """Takes url in queue and scrapes the content."""
    futures = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            url = article_urls_queue.get(timeout=2)
            if url is None:
                article_urls_queue.task_done()
                print("Empty queue. Exiting")
                break

            future = executor.submit(scrape_article_worker, url)
            futures.append(future)

        for future in as_completed(futures):
            try:
                data = future.result(timeout=5)
                print(data)
            except Exception as e:
                print("ERR", e)
            finally:
                article_urls_queue.task_done()
