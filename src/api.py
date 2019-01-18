#!/usr/bin/python3

import json
import requests
import sys
import time


class API:

    def __init__(self, api_key,
                 base_url="https://pro-api.coinmarketcap.com",
                 portfolio_dict=None,
                 initial_investment=0):

        self.api_key = {'X-CMC_PRO_API_KEY': api_key}
        self.base_url = base_url
        self.portfolio_dict = portfolio_dict
        self.initial_investment = initial_investment

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

        print(f"{coin_symbol} not found in portfolio.")

