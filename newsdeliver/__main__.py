import argparse
import asyncio
import sys
from newsdeliver.scraper import main, get_article

parser = argparse.ArgumentParser(prog="Newsdeliver", description="Newsdeliver is a news curator tool for building a corpus of news.")
parser.add_argument("-url", type=str, dest="feed_urls", nargs="+")

parser.add_argument("-article_url", type=str, dest="article_url", nargs="+")




args = parser.parse_args()

if args.article_url:
    asyncio.run(get_article(args.article_url))


if args.feed_urls:
    asyncio.run(main(args.feed_urls))


sys.exit()
