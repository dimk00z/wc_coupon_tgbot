import requests

from time import time
from datetime import timedelta, date
from transliterate import translit

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


def count_date_expires():
    end_date = date.today() + timedelta(days=31)
    return end_date.strftime("%Y-%m-%d")


def get_coupon_name(message) -> str:
    first_name_part = translit('_'.join(
        message.split()), 'ru', reversed=True)
    second_name_part = str(time())[:-8]
    coupon_name = f'{first_name_part}_{second_name_part}'
    return coupon_name


def get_coupon(
        wc_user_key: str,
        wc_secret_key: str,
        wc_url: str, message: str) -> str:

    auth_pair = (wc_user_key, wc_secret_key)
    url = f'{wc_url}/wp-json/wc/v3/coupons'
    coupon_name = get_coupon_name(message).upper()
    session = requests.Session()
    session.headers = HEADERS
    r = session.post(
        url, auth=auth_pair,
        params={
            "code": coupon_name,
            "discount_type": "percent",
            "amount": "10",
            "date_expires": count_date_expires(),
            "individual_use": True,
            "usage_limit": "1"
        })
    return coupon_name
