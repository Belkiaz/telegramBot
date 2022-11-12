import requests
import json

from config import keys, headers


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Переводить {quote} в {base} не представляется возможным. Это одно и то же')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработь валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалост обработать количество {amount}')

        r = requests.get(f'https://api.apilayer.com/exchangerates_data/latest?symbols={quote_ticker}&base={base_ticker}', headers=headers)

        r_json = json.loads(r.content)
        r_total = r_json['rates'][base_ticker] * float(amount)

        return r_total