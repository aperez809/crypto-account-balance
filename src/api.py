#!/usr/bin/env


import json
from pprint import pprint
import requests
import sys
import time


initial_investment = 0#sys.argv[1]
base = "https://pro.coinmarketcap.com"


def single_coin_val(currency_dict, coin):

    return round(float(requests.get
                       (base + currency_dict[coin][1]).json()[0]["price_usd"]) * currency_dict[coin][0], 2)


def account_values(currency_dict):
    """Return market data about currently held coins"""

    while True:
        total_val = 0.0
        for k,v in currency_dict.items():
            coin_val = round(float(requests.get(base+v[1]).json()[0]["price_usd"]) * v[0],2)
            total_val += coin_val
            print("Notional Account Value of {}: ${}".format(k, coin_val))

        print("\nProfit: ${} -> ${} ({}% change)\n\n\n\n\n".format(initial_investment, round(total_val, 2), round((total_val / initial_investment - 1) * 100, 2)))

        time.sleep(10)

def accountVales_DF(aDictOfCryptos):
    pass


class API:

    def __init__(self, api_key, base_url="https://pro-api.coinmarketcap.com", portfolio_dict=None):
        self.api_key = {'X-CMC_PRO_API_KEY': api_key}
        self.base_url = base_url
        self.portfolio_dict = portfolio_dict

    def get_all_currency_data(self):

        response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
                                headers={'X-CMC_PRO_API_KEY': '72f1177c-ac6c-467a-be24-7c4a9be270de'})

        if response.status_code != 200:
            raise ConnectionError(f"Connection failed with {response.status_code} error.")

        else:
            curr_data_list = json.loads(response.content)["data"]

        return curr_data_list

    def get_currency_ids(self):
        id_map = {}

        curr_data_list = self.get_all_currency_data()

        for item in curr_data_list:
            id_map[item["name"]] = item["symbol"]

        return id_map

    def portfolio_value(self):
        coin_values = {}

        curr_data_list = self.get_all_currency_data()

        for item in curr_data_list:
            if item["symbol"] in self.portfolio_dict.keys():
                coin_sym = item["symbol"]
                coin_values[coin_sym] = self.portfolio_dict[coin_sym] * item["quote"]["USD"]["price"]

        return coin_values

    def single_coin_value(self, coin_symbol):

        for item in self.get_all_currency_data():
            if item['symbol'] == coin_symbol:
                return item["quote"]["USD"]["price"]



conn = API("72f1177c-ac6c-467a-be24-7c4a9be270de",
           portfolio_dict={"ETH": 6.62523138,
                  "XRP": 501.493699,
                  "XRB": 44.58714468,
                  "OMG": 56.9,
                  "REQ": 661})

#print(conn.portfolio_value())
print(conn.single_coin_value("REQ"))
