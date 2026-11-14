import argparse
import asyncio
from scraper import main

parser = argparse.ArgumentParser(prog="Newsdeliver", description="Newsdeliver is an RSS scraper tool that can be used to build a corpus of news data for research.")
feed_urls = parser.add_argument("-url", type=str, )

parser = argparse.ArgumentParser(prog="Newsdeliver", description="Newsdeliver is an RSS scraper tool that can be used to build a corpus of news data for research.")
parser.add_argument("-url", type=str, dest="feed_urls", nargs="+")

args = parser.parse_args()

if __name__ == "__main__":
    if args.feed_urls:
        print(args.feed_urls)
        asyncio.run(main(args.feed_urls))