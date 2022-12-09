# Standard Library
import csv
import os
# Third-Party Libraries
import pandas as pd
import requests

def read_csv(path: str):
    return pd.read_csv(path).dropna()

def read_xls(path: str):
    return pd.read_excel(path, dtype=str).dropna()


def get_img_names(path):
    return os.listdir(path)


def add_row_to_csv(row, file_name):
    with open(file_name, "a+", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(row)


def get_sku(file_name):
    sku = file_name.split(".")[0]
    return sku

def download_img(uri, path, verify=True):

    with open(path, 'wb') as handle:
        response = requests.get(uri, stream=True,verify=verify)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)