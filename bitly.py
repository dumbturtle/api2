import argparse
import os
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


def cut_bitlink(user_link):
    http_link = "http"
    processed_link = user_link
    if user_link.startswith(http_link):
        processed_link = f"{urlparse(user_link).netloc}{urlparse(user_link).path}"
    return processed_link


def is_bitlink(user_link, bitly_api_token):
    cut_user_link = cut_bitlink(user_link)
    headers = {"Authorization": f"Bearer { bitly_api_token }"}
    bit_link = f"https://api-ssl.bitly.com/v4/bitlinks/{ cut_user_link }/clicks"
    bitly_api_response = requests.get(bit_link, headers=headers)
    return bitly_api_response.ok


def create_short_link(user_link, api_bitly, bitly_api_token):
    headers = {"Authorization": f"Bearer { bitly_api_token }"}
    bitly_user_link = {"long_url": user_link}
    bitly_api_response = requests.post(api_bitly, headers=headers, json=bitly_user_link)
    bitly_api_response.raise_for_status()
    bitly_short_link = bitly_api_response.json().get("link")
    return bitly_short_link


def count_clicks_link(user_link, bitly_api_token):
    headers = {"Authorization": f"Bearer { bitly_api_token }"}
    cut_user_link = cut_bitlink(user_link)
    bitly_api_click_url = (
        f"https://api-ssl.bitly.com/v4/bitlinks/{ cut_user_link }/clicks/summary"
    )
    bitly_api_response = requests.get(bitly_api_click_url, headers=headers)
    bitly_api_response.raise_for_status()
    bitly_sum_clicks = bitly_api_response.json().get("total_clicks")
    return bitly_sum_clicks


def process_query_link(user_link, bitly_api_token, bitly_api, error_message):
    if is_bitlink(user_link, bitly_api_token):
        quantity_clicks_link = count_clicks_link(user_link, bitly_api_token)
        return f"Количество переходов: { quantity_clicks_link }"
    short_link = create_short_link(user_link, bitly_api, bitly_api_token)
    return f"Краткая ссылка: { short_link }"


def main():
    load_dotenv()
    bitly_api_token = os.getenv("BITLY_API_TOKEN")
    error_message = os.getenv("ERROR_TEXT")
    bitly_api_url = os.getenv("BILTY_API_URL")
    commandline_parser = create_commandline_parser()
    user_arguments = commandline_parser.parse_args()
    user_link = user_arguments.asked_url
    try:
        message = process_query_link(
            user_link, bitly_api_token, bitly_api_url, error_message
        )
    except requests.exceptions.HTTPError:
        message = error_message
    print(message)


if __name__ == "__main__":
    main()
