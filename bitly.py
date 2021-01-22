import argparse
import json
import os
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "asked_url",
        help="Укажите ссылку для уменьшения или адрес для проверки кол-ва переходов. Пример: https://google.com",
    )
    return parser


def convert_bitlink(link):
    link_https = "https"
    if link.startswith(link_https):
        link = f"{urlparse(link).netloc}{urlparse(link).path}"
    return link


def is_bitlink(link, token):
    link = convert_bitlink(link)
    headers = {"Authorization": f"Bearer { token }"}
    bit_link = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks"
    response_data = requests.get(bit_link, headers=headers)
    return response_data.ok


def shorten_link(url, token):
    headers = {"Authorization": f"Bearer { token }"}
    bitly_url = {"long_url": url}
    response_data = requests.post(
        os.getenv("LINK_URL"), headers=headers, json=bitly_url
    )
    response_data.raise_for_status()
    bitly_link = response_data.json().get("link")
    return bitly_link


def count_clicks_link(link, token):
    headers = {"Authorization": f"Bearer { token }"}
    sum_clicks = 0
    link = convert_bitlink(link)
    bit_link = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks"
    response_data = requests.get(bit_link, headers=headers)
    response_data.raise_for_status()
    clicks = response_data.json().get("link_clicks")
    for click in clicks:
        sum_clicks = sum_clicks + click.get("clicks", 0)
    return sum_clicks


def handler_url(url):
    try:
        if is_bitlink(url, os.getenv("TOKEN")):
            count_clicks = count_clicks_link(url, os.getenv("TOKEN"))
            clicks = f"Количество переходов: { count_clicks }"
            return clicks
        link = shorten_link(url, os.getenv("TOKEN"))
        bitly_link = f"Краткая ссылка: { link }"
        return bitly_link
    except requests.exceptions.HTTPError:
        message_error = os.getenv("ERROR_TEXT")
        return message_error


def main():
    load_dotenv()
    parser = createParser()
    namespace = parser.parse_args()
    bitly_url = namespace.asked_url
    print(handler_url(bitly_url))


if __name__ == "__main__":
    main()
