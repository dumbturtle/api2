import argparse
import json
import os
import sys
from urllib.parse import urlparse

import requests

import settings


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "asked_url",
        help="Укажите ссылку для уменьшения или адрес для проверки кол-ва переходов. Пример: https://google.com",
    )

    return parser


def shorten_link(url, token):
    headers = {"Authorization": f"Bearer { token }"}
    bilty_url = {"long_url": url}
    response_data = requests.post(os.getenv("LINK_URL"), headers=headers, json=bilty_url)
    response_data.raise_for_status()
    bilty_link = response_data.json().get("link")
    return bilty_link


def count_clicks(link, token):
    headers = {"Authorization": f"Bearer { token }"}
    bitlink_url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks"
    params = {
        "unit": "day",
        "units": 1,
    }
    response_data = requests.get(bitlink_url, headers=headers, params=params)
    response_data.raise_for_status()
    clicks_count = response_data.json().get("link_clicks")[0].get("clicks")
    return clicks_count


def handler_url(url):
    bilty_url = "bit.ly"
    bilty_url_https = "https://bit.ly"
    if url.startswith(bilty_url_https):
        url = f"{urlparse(url).netloc}{urlparse(url).path}"
    if url.startswith(bilty_url):
        try:
            clicks = f"Количество переходов: {count_clicks(url, os.getenv('TOKEN'))}"
        except requests.exceptions.HTTPError:
            clicks = os.getenv("ERROR_TEXT")
        return clicks
    try:
        short_url = f"Краткая ссылка: {shorten_link(url, os.getenv('TOKEN'))}"
    except requests.exceptions.HTTPError:
        short_url = os.getenv("ERROR_TEXT")
    return short_url


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()
    bilty_url = namespace.asked_url
    print(handler_url(bilty_url))
