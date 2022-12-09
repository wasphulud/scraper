# Standard Library
import json
import os

# Third-Party Libraries
import requests
from tqdm import tqdm

# Project Imports
from image_scraper.helpers import add_row_to_csv, get_img_names, get_sku


def build_files(root_imgs, img_name):
    img_path = os.path.join(root_imgs, img_name)
    return {"image": (img_name, open(img_path, "rb"), "image/jpg")}


def extract_uri(rest_response):
    parsed_data = rest_response.text.strip("][").split(", ")[0]
    converted_data = json.loads(parsed_data)
    print(converted_data)
    uri = converted_data["data"]["url"]
    return uri


def upload_img(
    roots,
    img_name,
    url="https://api.imgbb.com/1/upload?key=c2d7c976a0a605c2f4e4e39217bb23f3",
):
    files = build_files(roots, img_name)
    print(img_name)
    response = requests.post(url, files=files)
    img_uri = extract_uri(response)
    return img_uri


def upload(root_imgs, output_file, api_key="c2d7c976a0a605c2f4e4e39217bb23f3"):
    url = "https://api.imgbb.com/1/upload?key=" + api_key

    imgs_names = get_img_names(root_imgs)
    for img_name in tqdm(imgs_names):
        img_uri = upload_img(root_imgs, img_name, url)
        sku = get_sku(img_name)
        add_row_to_csv([sku, img_uri], output_file)
