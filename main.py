# Standard Library
import os
import sys
from argparse import ArgumentParser

# Project Imports
from scraper.scrape import Scraper


def parse_args(args):
    parser = ArgumentParser()
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    with Scraper() as scraper:
        scraper.scrape()


if __name__ == "__main__":
    main(sys.argv[1:])
