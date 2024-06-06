# Text Search Image Scraper

## Introduction
This repository contains a Python script designed to scrape images from Google based on any predefined text search. Initially created to help a friend gather logos, this tool can be utilized for a wide range of search queries.

# Description
This repo helps a user download google images by providing a list of google queries in a csv format.
* One can tweak the max-workers to use concurrent processing. The usual sweet spot is the half the total number of the avaialble CPUs
* One may want to adjust the version of chromedriver-py depending on your own chrome version.

TODO:
* pylint
* DocString
* Type hints
* Refactor
* Package
* How to

For immediate use, one can run the command below
```python
python main.py --xls PATH/TO/XLSX --output PATH/TO/FOLDER/WHERE/TO/SAVE/THE/IMAGES  --max-workers NUM_CPUS
```
