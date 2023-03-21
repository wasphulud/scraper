# Standard Library
import logging
import os
import urllib.request
from random import random
from time import sleep
import time
from multiprocessing import Process
from selenium.webdriver.chrome.options import Options

# Third-Party Libraries
import pandas as pd
import numpy as np
import unidecode
from selenium import webdriver


logger = logging.getLogger(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")

GOOGLE_XPATH_IMAGE = '//img[contains(@class,"rg_i Q4LuWd")]'
EMPTY_RESEARCH_GOOGLE = '//*[@id="islmp"]/div/div/p[1]'

LOCAL_TIME = time.ctime(time.time())


class Scraper:
    def __init__(self, max_candidates: int = 1, chromedriver: str = ""):
        self.browser = None
        self.entered = False
        self.max_candidates = max_candidates
        self.skip = False
        self.chromedriver = chromedriver

    def __enter__(self):
        self.browser = webdriver.Chrome(self.chromedriver, options=chrome_options)
        self.entered = True
        return self

    def __exit__(self, *args):
        # cleanup browser
        self.browser.close()
        self.browser = None
        self.entered = False

    def word_sanity(self, word):
        word = unidecode.unidecode(word)
        return (
            word.replace("/", "-")
            .replace("®", "")
            .replace("�", "")
            .replace('"', "")
            .replace("@", "")
            .replace("&", "")
        )

    def scrape(self, df: pd.DataFrame, output_path: str):
        # print(df.head())
        if not self.entered:
            raise Exception("Not entered, browser not initialized")

        for _id, name, actor, searchterm, *_ in df.itertuples():
            if self.skip:
                if name == "escape":
                    self.skip = False
                    print("Skipping for the last time")
                else:
                    print(f"Skipping {name, actor}")
                continue

            self.google_scrape(
                term=searchterm, output_path=output_path, name=name, line_num=_id
            )

            # sleep(random())

    def google_scrape(self, term, output_path, name, line_num):
        url = f"https://www.google.co.in/search?q={term}&source=lnms&tbm=isch"
        self.browser.get(url)
        try:
            element_all_accept = self.browser.find_element(
                "xpath",
                '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span',
            )
            element_all_accept.click()
        except Exception as e:
            # print("Occured Exception",e )
            pass

        try:
            elements_imgs = self.browser.find_element("xpath", GOOGLE_XPATH_IMAGE)

            new_filename = f"{name}.png"
            if name is not None:
                new_filename = name + ".png"

            # print(elements_imgs)
            # logger.info("URL:", x.get_attribute("src"))
            uri = elements_imgs.get_attribute("src")

            path = os.path.join(output_path, "downloads", new_filename)
            urllib.request.urlretrieve(uri, path)
            print("google image successfully downloaded locally")
        except Exception as e:
            with open(os.path.join(output_path, f"report_{LOCAL_TIME}.txt"), "a") as fd:
                fd.write(f"\n\n Issue with line {line_num+1} with ID {name}")
                fd.write(f"\n error: {e}")
            # print("#####################", e)

        # uri = upload_img(os.path.join(output_path, "downloads"), new_filename)


def multiscraper(dataframe, num_process, max_candidates, chromedriver, output):
    dataframes = np.array_split(dataframe, num_process)
    processes = []
    for i, dataframe in enumerate(dataframes):
        process = Process(
            target=run_single_scraper,
            args=(dataframe, max_candidates, chromedriver, output, i),
        )
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f"All Processes have been terminated", flush=True)


def run_single_scraper(dataframe, max_candidates, chromedriver, output, i):
    print(f"Starting process {i}", flush=True)
    with Scraper(max_candidates, chromedriver) as scraper:
        scraper.scrape(dataframe, output)
    print(f"Finishing process {i}", flush=True)
