# Standard Library
import logging
import os
import urllib.request
from random import random
from time import sleep, time
from datetime import datetime

# Third-Party Libraries
import pandas as pd
import unidecode
from selenium import webdriver


from scraper.helpers import send_email

CHECKBOX_XPATH = '//*[@id="condition"]'
SUBMIT_BUTTON_XPATH = '//*[@id="submit_Booking"]/input[1]'
NO_AVAILABLE_SLOT_URLS = ['https://pprdv.interieur.gouv.fr/booking/create/948/2', 'http://pprdv.interieur.gouv.fr/booking/create/948/2', 'https://pprdv.interieur.gouv.fr/booking/create/948/1', 'http://pprdv.interieur.gouv.fr/booking/create/948/1']
AVAILABLE_SLOT_URLS = 'https://pprdv.interieur.gouv.fr/booking/create/948/4'
ADMISSION_EXCEPTIONNELLE_VPF_XPATH = '//*[@id="fchoix_Booking"]/p/label'
SUBMIT_BUTTON_ADMISSION_VPF = '//*[@id="submit_Booking"]/input'
class Scraper:
    def __init__(self, max_candidates: int = 1):
        self.browser = None
        self.entered = False

    def __enter__(self):
        self.browser = webdriver.Chrome()
        self.entered = True
        return self

    def __exit__(self, *args):
        # cleanup browser
        self.browser.close()
        self.browser = None
        self.entered = False

    def submit_normal_one(self):
        if not self.entered:
            raise Exception("Not entered, browser not initialized")

        url = f"https://pprdv.interieur.gouv.fr/booking/create/948"
        try:
            self.browser.get(url)
            element_checkbox = self.browser.find_elements_by_xpath(
                CHECKBOX_XPATH
            )
            if len(element_checkbox) > 0:
                element_cb = element_checkbox[0]
                element_cb.location_once_scrolled_into_view
                element_cb.click()
                sleep(1)
                element_submit = self.browser.find_elements_by_xpath(
                    SUBMIT_BUTTON_XPATH
                )
                element_sb = element_submit[0]
                #element_sb.location_once_scrolled_into_view
                element_sb.click()

                #sleep(2)
                current_url = self.browser.current_url 

                """if current_url == NO_AVAILABLE_SLOT_URLS[0]:
                    print("[SUBMIT-NORMAL] Désolé, Il n'y a pas encore de plage disponible pour le moment 1 (https)... ")
                elif current_url == NO_AVAILABLE_SLOT_URLS[1]:
                    print("[SUBMIT-NORMAL] Désolé, Il n'y a pas encore de plage disponible pour le moment 2 (http)... ")
                elif current_url == NO_AVAILABLE_SLOT_URLS[2]:
                    print("[SUBMIT-NORMAL] Désolé, Il n'y a pas encore de plage disponible pour le moment 3 (http)... ")
                elif current_url == NO_AVAILABLE_SLOT_URLS[2]:
                    print("[SUBMIT-NORMAL] Désolé, Il n'y a pas encore de plage disponible pour le moment 3 (http)... ")"""
                if current_url==AVAILABLE_SLOT_URLS:
                    send_email()
                    self.browser.save_screenshot(f"/Users/aiman/Desktop/MyFolders/code/scrapper/screenshots/img_{datetime.now().isoformat(timespec='seconds')}.png")
                    print("[SUBMIT-NORMAL] ########################################## YOUUUHOUUUUUUUUUU, VITE INSCRIT TOOOOOOOUUUUUUUUUUUUAAAAAAA ... ##########################################")
                    print(f'current url {current_url}')
                    self.browser.get(current_url)
                    print(self.browser.page_source)
                    print('sleeping ... 10 min')
                    sleep(60*10)
                else:
                    print("[SUBMIT-NORMAL] Désolé, Il n'y a pas encore de plage disponible pour le moment ... ")
                    print(f"[SUBMIT-NORMAL] Current url {current_url}")
            else:
                print("[SUBMIT-NORMAL] Désolé, Il n'y a pas encore de plage disponible pour le moment 3... ")
                self.browser.save_screenshot(f"/Users/aiman/Desktop/MyFolders/code/scrapper/screenshots/failiure_normal_{datetime.now().isoformat(timespec='seconds')}.png")

        except Exception as e:
            print(f'an error occurs {e}')
            self.browser.save_screenshot(f"/Users/aiman/Desktop/MyFolders/code/scrapper/screenshots/failiure_normal_{datetime.now().isoformat(timespec='seconds')}.png")

            

    def submit_vpf_one(self):
        if not self.entered:
            raise Exception("Not entered, browser not initialized")

        url = f"https://pprdv.interieur.gouv.fr/booking/create/948/1"
        try:
            self.browser.get(url)
            element_checkbox = self.browser.find_elements_by_xpath(
                ADMISSION_EXCEPTIONNELLE_VPF_XPATH
            )
            if len(element_checkbox) > 0:
                element_cb = element_checkbox[0]
                element_cb.location_once_scrolled_into_view
                element_cb.click()
                sleep(1)
                element_submit = self.browser.find_elements_by_xpath(
                    SUBMIT_BUTTON_ADMISSION_VPF
                )
                element_sb = element_submit[0]
                #element_sb.location_once_scrolled_into_view
                element_sb.click()

                #sleep(2)
                current_url = self.browser.current_url 
                

                """if current_url == NO_AVAILABLE_SLOT_URLS[0]:
                    print("[SUBMIT-VPF] Désolé, Il n'y a pas encore de plage disponible pour le moment 1 (https)... ")
                elif current_url == NO_AVAILABLE_SLOT_URLS[1]:
                    print("[SUBMIT-VPF] Désolé, Il n'y a pas encore de plage disponible pour le moment 2 (http)... ")"""
                if current_url==AVAILABLE_SLOT_URLS:
                    send_email()
                    self.browser.save_screenshot(f"/Users/aiman/Desktop/MyFolders/code/scrapper/screenshots/img_{datetime.now().isoformat(timespec='seconds')}.png")
                    print("[SUBMIT-VPF] ##########################################  YOUUUHOUUUUUUUUUU, VITE INSCRIT TOOOOOOOUUUUUUUUUUUUAAAAAAA ... ##########################################")
                    print(f'current url {current_url}')
                    self.browser.get(current_url)
                    print(self.browser.page_source)
                    print('sleeping ... 10 min')
                    sleep(10*60)
                else:
                    print("[SUBMIT-VPF] Désolé, Il n'y a pas encore de plage disponible pour le moment ... ")
                    print(f"[SUBMIT-VPF] Current url {current_url}")
            else:
                print("[SUBMIT-VPF] Désolé, Il n'y a pas encore de plage disponible pour le moment 3 ... ")
                self.browser.save_screenshot(f"/Users/aiman/Desktop/MyFolders/code/scrapper/screenshots/failiure_vpf_{datetime.now().isoformat(timespec='seconds')}.png")
        except Exception as e:
            print(f'an error occurs {e}')
            self.browser.save_screenshot(f"/Users/aiman/Desktop/MyFolders/code/scrapper/screenshots/failiure_vpf_{datetime.now().isoformat(timespec='seconds')}.png")

            
    def scrape(self):
        i = 23827
        while True:
            i +=1
            print(f"[SUBMIT-NORMAL] Test {i}, ...")
            print(datetime.now().isoformat(timespec='seconds'))
            self.submit_normal_one()
            print("sleep 30s")
            sleep(30)

            i +=1 
            print(f"[SUBMIT-VPF] Test {i}, ...")
            print(datetime.now().isoformat(timespec='seconds'))
            self.submit_vpf_one()
            print(" sleep 30")
            sleep(30)

