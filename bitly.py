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


def cut_bitlink(link):
    https_link = "https"
    if link.startswith(https_link):
        link = f"{urlparse(link).netloc}{urlparse(link).path}"
    return link


def is_bitlink(link, token):
    link = cut_bitlink(link)
    headers = {"Authorization": f"Bearer { token }"}
    bit_link = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks"
    bitly_api_response = requests.get(bit_link, headers=headers)
    return bitly_api_response.ok


def create_short_link(url, api_bitly, token):
    headers = {"Authorization": f"Bearer { token }"}
    bitly_url = {"long_url": url}
    bitly_api_response = requests.post(api_bitly, headers=headers, json=bitly_url)
    bitly_api_response.raise_for_status()
    bitly_short_link = bitly_api_response.json().get("link")
    return bitly_short_link


def count_link_clicks(link, token):
    headers = {"Authorization": f"Bearer { token }"}
    bitly_sum_clicks = 0
    user_link = cut_bitlink(link)
    bitly_api_click_url = f"https://api-ssl.bitly.com/v4/bitlinks/{user_link}/clicks"
    bitly_api_response = requests.get(bitly_api_click_url, headers=headers)
    bitly_api_response.raise_for_status()
    bitly_clicks = bitly_api_response.json().get("link_clicks")
    for click in bitly_clicks:
        bitly_sum_clicks = bitly_sum_clicks + click.get("clicks", 0)
    return bitly_sum_clicks


def process_query_link(link, token, api_bitly, message_error):
    try:
        if is_bitlink(link, token):
            quantity_link_clicks = count_link_clicks(link, token)
            return f"Количество переходов: { quantity_link_clicks }"
        short_link = create_short_link(link, api_bitly, token)
        return f"Краткая ссылка: { short_link }"
    except requests.exceptions.HTTPError:
        return message_error


def main():
    load_dotenv()
    bitly_api_token = os.getenv("BITLY_API_TOKEN")
    message_error = os.getenv("ERROR_TEXT")
    bitly_api = os.getenv("LINK_URL")
    commandline_parser = create_commandline_parser()
    user_arguments = commandline_parser.parse_args()
    user_link = user_arguments.asked_url
    message = process_query_link(user_link, bitly_api_token, bitly_api, message_error)
    print(message)


if __name__ == "__main__":
    main()
