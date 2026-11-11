from .scraper import orchestrate_rss_workers, orchestrate_article_workers
from queue import Queue
from threading import Thread

if __name__=="__main__":
    import httpx

    feed_urls = [

        #"https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=Iran",
        "https://feeds.skynews.com/feeds/rss/uk.xml",
        #"https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://feeds.bbci.co.uk/news/rss.xml"
    ]

    article_urls_queue = Queue(maxsize=20)
    with httpx.Client() as client:

            consumer = Thread(target=orchestrate_article_workers, args=(article_urls_queue,))
            consumer.start()
            orchestrate_rss_workers(client, feed_urls, article_urls_queue)

            article_urls_queue.put(None)
            print(f"Article URLs in queue: {article_urls_queue.qsize()}")
            print("Waiting for consumer to finish...")
            consumer.join()
            print("Consumer finished. Exiting...")


