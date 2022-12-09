# Standard Library
import logging
import os
import urllib.request
from random import random
from time import sleep

# Third-Party Libraries
import pandas as pd
import unidecode
from selenium import webdriver

# Project Imports
from image_scraper.helpers import add_row_to_csv, download_img
from image_scraper.imgbb_uploader import upload_img

logger = logging.getLogger(__name__)

BARCODE_UPCITEMBD_XPATH_NAME = (
    '/html/body/div[1]/div/div[1]/div[3]/div/ol/li[1]'
)
BARCODE_UPCITEMBD__XPATH_IMAGE = '/html/body/div[1]/div/div[1]/div[1]/img'
BARCODE_UPCITEMBD_NO_AVAILABLE_IMAGE  = 'https://www.upcitemdb.com/static/img/resize.jpg'
BARCODE_LOOKUP_XPATH_NAME = (
    '//*[@id="body-container"]/section[2]/div/div/div[2]/h4'
)
BARCODE_LOOKUP_XPATH_IMAGE = '//*[@id="img_preview"]'
BARCODE_LOOKUP_NO_AVAILABLE_IMAGE = (
    "https://www.barcodelookup.com/assets/images/no-image-available.jpg"
)
BARCODE_GOOGLE_XPATH_IMAGE = '//img[contains(@class,"rg_i Q4LuWd")]'
EMPTY_RESEARCH_GOOGLE = '//*[@id="islmp"]/div/div/p[1]'

class Scraper:
    def __init__(self, max_candidates: int = 1):
        self.browser = None
        self.entered = False
        self.max_candidates = max_candidates
        self.skip = True

    def __enter__(self):
        self.browser = webdriver.Chrome()
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
            .replace("\"", "")
            .replace("@", "")
            .replace("&", "")
        )

    def scrape(self, df: pd.DataFrame, output_path: str, upload_all=True):
        if not self.entered:
            raise Exception("Not entered, browser not initialized")
        for i, sku, *_ in df.itertuples():
            if self.skip:
                if sku == 'escape':
                    self.skip = False
                    print(f'Skipping for the last time')
                else:
                    print(f'Skipping {sku}')
                continue
            searchterm = sku  # will also be the name of the folder
            url = f"https://www.barcodelookup.com/{searchterm}"
            self.browser.get(url)
            element_name = self.browser.find_elements_by_xpath(
                BARCODE_LOOKUP_XPATH_NAME
            )
            if element_name == []:
                print(sku, "product NOT available in the barcode lookup, searching in UPCITEMBD ... ")
                uri_origin, name, found = self.upcitemdb_scrape(searchterm)
                if not found:
                    print(sku, "product NOT available in the barcode lookup neither UPCITEMBD, scraping google")
                    uri_origin = 'google.com'
                    uri = self.google_scrape(
                        sku=searchterm, output_path=output_path
                    )
                    name = sku
            else:
                print(sku, "product available in the barcode lookup")
                name = element_name[0].text
                name = self.word_sanity(name)
                elements_imgs = self.browser.find_elements_by_xpath(
                    BARCODE_LOOKUP_XPATH_IMAGE
                )
                for x in elements_imgs:
                    logger.info("URL:", x.get_attribute("src"))
                    uri_origin = x.get_attribute("src")
                    if uri_origin == BARCODE_LOOKUP_NO_AVAILABLE_IMAGE:
                        print("Image NOT available, using upcitemdb images ...")
                        uri_origin, _, found = self.upcitemdb_scrape(searchterm)
                        if not found or uri_origin == BARCODE_UPCITEMBD_NO_AVAILABLE_IMAGE:
                            print("Image NOT available in UPCITEMBD, using google images ...")
                            uri = self.google_scrape(
                                sku=searchterm,
                                name=name,
                                output_path=output_path,
                            )
                            uri_origin = "google.com"
                        else:
                            filename = name + '.png'
                            download_img(uri_origin, os.path.join(output_path, "downloads", filename), False)
                            #uri = upload_img(os.path.join(output_path, "downloads"), filename)
                            uri = os.path.join(output_path, "downloads", filename) #put local address
                    else:
                        filename = name + '.png'
                        download_img(uri_origin, os.path.join(output_path, "downloads", filename), False)
                        #uri = upload_img(os.path.join(output_path, "downloads"), filename)
                        uri = os.path.join(output_path, "downloads", filename) #put local address



            print("barcode: ", sku, "name: ", name, "link origin: ", uri_origin, "link: ", uri)
            add_row_to_csv(
                [sku, name, uri], os.path.join(output_path, "db.csv")
            )
            add_row_to_csv(
                [sku, name, uri_origin], os.path.join(output_path, "db_origin_uris.csv")
            )
            sleep(random() * 10)

    def google_scrape(self, sku, output_path, name=None):
        url = f"https://www.google.co.in/search?q={sku}&source=lnms&tbm=isch"
        self.browser.get(url)
        elements_imgs = self.browser.find_elements_by_xpath(
            BARCODE_GOOGLE_XPATH_IMAGE
        )
        new_filename = f"{sku}.png"
        if name is not None:
            new_filename = name + ".png"
        for x in elements_imgs:
            logger.info("URL:", x.get_attribute("src"))
            uri = x.get_attribute("src")
            try:
                path = os.path.join(output_path, "downloads", new_filename)
                urllib.request.urlretrieve(uri, path)
                print("google image successfully downloaded locally")
            except Exception as e:
                print("#####################", e)
            #uri = upload_img(os.path.join(output_path, "downloads"), new_filename)
            uri = os.path.join(output_path, "downloads", new_filename) #put local address

            print("Image successfully uploadedd to imgbb")
            return uri
        empty_research_elements = self.browser.find_elements_by_xpath(EMPTY_RESEARCH_GOOGLE)
        for x in empty_research_elements:
            text = x.text
            print(text)
            return None
        print("INPUT IS NEEDED")
        input()
        return None

    def upcitemdb_scrape(self, searchterm):
        url = f'https://www.upcitemdb.com/upc/{searchterm}'
        self.browser.get(url)
        elements_imgs = self.browser.find_elements_by_xpath(BARCODE_UPCITEMBD__XPATH_IMAGE)
        for element_img in elements_imgs:
            uri = element_img.get_attribute("src")
            elements_name = self.browser.find_elements_by_xpath(BARCODE_UPCITEMBD_XPATH_NAME)
            for element_name in elements_name:
                name = element_name.text
                return uri, name, True
        return searchterm, searchterm, False
