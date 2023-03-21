# Standard Library
import os
import sys
from argparse import ArgumentParser
from time import perf_counter

# Project Imports
from helpers import read_csv, read_xls
from scrape_google import Scraper, multiscraper


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument("--csv", type=str, default=os.getenv("CSV_INPUT"))
    parser.add_argument("--xls", type=str, default=os.getenv("xls_INPUT"))
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        default=os.getenv("IMAGES_OUTPUT_PATH"),
    )
    parser.add_argument(
        "--max_candidates",
        type=int,
        default=os.getenv("IMAGES_MAX_CANDIDATES", 1),
    )
    parser.add_argument(
        "--chromedriver",
        type=str,
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=1,
    )
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    if args.csv:
        dataframe = read_csv(args.csv)
    elif args.xls:
        dataframe = read_xls(args.xls)
    else:
        print("NO INPUT FOUND")

    # with Scraper(args.max_candidates, args.chromedriver) as scraper:
    #    scraper.scrape(dataframe, args.output)

    # without headless chrome VS headless chrome
    # performance on my computer with 1 processor = 98.5s | 100 for 59 query
    # performance on my computer with 3 processor = 55.11 | 53.9 for 59 query
    # performance on my computer with 4 processors =  56.3 | 51 for 59 query
    # performance on my computer with 5 processors =  57.2 |  48 for 59 query
    # performance on my computer with 6 processors =  62.5 |  51 for 59 query
    # performance on my computer with 9 processors (all my cpus) =  79.2 |  60 for 59 query
    # performance on my computer with 12 processors (all my cpus) =  99 |  69 for 59 query
    # performance on my computer with 20 processors  =  195.9 (CPU bound) | 107 for 59 query

    start_time = perf_counter()
    multiscraper(
        dataframe, args.max_workers, args.max_candidates, args.chromedriver, args.output
    )
    print(f"Total time: {perf_counter() - start_time} seconds")


if __name__ == "__main__":
    main(sys.argv[1:])
