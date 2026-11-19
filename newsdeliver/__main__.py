import argparse
import asyncio
import sys
from newsdeliver.scraper import main

parser = argparse.ArgumentParser(prog="Newsdeliver", description="Newsdeliver is a news curator tool for building a corpus of news.")
parser.add_argument("-url", type=str, dest="feed_urls", nargs="+")

args = parser.parse_args()

if args.feed_urls:
    print(args.feed_urls)
    asyncio.run(main(args.feed_urls))


sys.exit()
