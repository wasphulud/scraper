# scraper

This repo helps a user download google images by providing a list of google queries in a csv format.
One can tweak the max-workers to use concurrent processing. The usual sweet spot is the half the total number of the avaialble CPUs

TODO:
* pylint
* DocString
* Type hints
* Refactor
* Package
* How to

For immediate use, one can run the command below
```python
python main.py --xls PATH/TO/XLSX --output PATH/TO/FOLDER/WHERE/TO/SAVE/THE/IMAGES --chromedriver PATH/TO/CHROMEDRIVER --max-workers NUM_CPUS
```
