# Standard Library
import os
import sys
from argparse import ArgumentParser

# Project Imports
from helpers import read_csv, read_xls
from scrape_google import Scraper


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument(
        "--csv", type=str, default=os.getenv("CSV_INPUT")
    )
    parser.add_argument(
        "--xls", type=str, default=os.getenv("xls_INPUT")
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        default=os.getenv("IMAGES_OUTPUT_PATH"),
    )
    parser.add_argument(
        "--max_candidates",
        type=int,
        default=os.getenv("IMAGES_MAX_CANDIDATES_PER_SKU", 1),
    )
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    with Scraper(args.max_candidates) as scraper:
        if args.csv:
            scraper.scrape(read_csv(args.csv), args.output)
        elif args.xls:
            scraper.scrape(read_xls(args.xls), args.output)
        else:
            print('no input found')



if __name__ == "__main__":
    main(sys.argv[1:])
