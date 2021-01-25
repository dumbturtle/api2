import argparse
import json
import os
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def create_commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "asked_url",
        help="Укажите ссылку для уменьшения или адрес для проверки кол-ва переходов. Пример: https://google.com",
    )
    return parser


def cut_bitlink(link):
    link_https = "https"
    if link.startswith(link_https):
        link = f"{urlparse(link).netloc}{urlparse(link).path}"
    return link


def is_bitlink(link, token):    
    link = cut_bitlink(link)
    headers = {"Authorization": f"Bearer { token }"}
    bit_link = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks"
    response_bitly = requests.get(bit_link, headers=headers)
    return response_bitly.ok


def create_short_link(url, api_bitly, token):
    headers = {"Authorization": f"Bearer { token }"}
    bitly_url = {"long_url": url}
    response_bitly = requests.post(api_bitly, headers=headers, json=bitly_url)
    response_bitly.raise_for_status()
    bitly_link = response_bitly.json().get("link")
    return bitly_link


def count_clicks_link(link, token):
    headers = {"Authorization": f"Bearer { token }"}
    sum_clicks = 0
    link = cut_bitlink(link)
    bitly_api_click_url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks"
    response_bitly = requests.get(bitly_api_click_url, headers=headers)
    response_bitly.raise_for_status()
    clicks = response_bitly.json().get("link_clicks")
    for click in clicks:
        sum_clicks = sum_clicks + click.get("clicks", 0)
    return sum_clicks


def process_query_link(link, token, api_bitly, message_error):
    try:
        if is_bitlink(link, token):
            count_clicks = count_clicks_link(link, token)
            clicks = f"Количество переходов: { count_clicks }"
            return clicks
        short_link = create_short_link(link, api_bitly, token)
        bitly_link = f"Краткая ссылка: { short_link }"
        return bitly_link
    except requests.exceptions.HTTPError:
        return message_error


def main():
    load_dotenv()
    bitly_api_token = os.getenv("BITLY_API_TOKEN")
    message_error = os.getenv("ERROR_TEXT")
    api_bitly = os.getenv("LINK_URL")
    commandline_parser = create_commandline_parser()
    user_arguments = commandline_parser.parse_args()
    bitly_link = user_arguments.asked_url
    message = process_query_link(bitly_link, bitly_api_token, api_bitly, message_error)
    print(message)


if __name__ == "__main__":
    main()
