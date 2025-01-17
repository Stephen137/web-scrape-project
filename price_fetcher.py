import requests as r
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass
from typing import List
from exchange_rate_fetcher import fetch_exchange_rate

# Fetch coin price
def fetch_coin_price(coin_symbol):
    url = f"https://coinmarketcap.com/currencies/{coin_symbol}/"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    price_span = soup.find("span", {"data-test": "text-cdp-price-display"})
    price_dollars = price_span.text.strip()
    return float(re.sub("[^0-9.]", "", price_dollars))

# Define the Coin class
@dataclass
class Coin:
    coin_symbol: str
    target_currency: str = "GBP"
    usd_price: float = 0
    target_currency_price: float = 0

    def __post_init__(self):
        fx = fetch_exchange_rate(self.target_currency)
        usd_price = fetch_coin_price(self.coin_symbol)
        self.usd_price = usd_price
        self.target_currency_price = round(usd_price * fx, 3)

# Define the Position class
@dataclass
class Position:
    coin: Coin
    quantity: float

# Define the Portfolio class
@dataclass
class Portfolio:
    positions: List[Position]

    def get_total_value(self):
        return sum(position.quantity * position.coin.target_currency_price for position in self.positions)