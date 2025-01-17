# Import required libraries
import requests as r
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
import datetime as dt
from tabulate import tabulate

# Parse date for portfolio valuation timestamping
now = dt.datetime.now()
hour = now.hour
minute = now.minute 

# Helper function to parse exchange rate
def exchange_from_dollar(target_currency):
    
    fx_url = f"https://www.google.com/finance/quote/USD-{target_currency}"
    resp = r.get(fx_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    fx_rate = soup.find("div", attrs={"data-last-price": True})
    fx = float(fx_rate["data-last-price"])
    
    return fx

# Helper function to parse the crypto price data
def get_price_info(coin_symbol, target_currency):
    
    fx = exchange_from_dollar(target_currency)
    url = f"https://coinmarketcap.com/currencies/{coin_symbol}/"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    # Locate the span using the `data-test` attribute
    price_span = soup.find("span", {"data-test": "text-cdp-price-display"})
    price_dollars = price_span.text.strip()
    usd_price = float(re.sub("[^0-9.]", "", price_dollars))
    target_currency_price = round(usd_price * fx, 3)
          
    return {
        "coin_symbol": coin_symbol,
        "usd_price": usd_price,
        "target_currency": target_currency,
        "target_currency_price": target_currency_price        
    }


# Create a custom class for the Coins
@dataclass
class Coin:
    coin_symbol: str
    #price: float = 0  # default values
    target_currency: str = "GBP" # *** AMEND THIS AS REQUIRED ***
    usd_price: float = 0  # default values
    target_currency_price: float = 0

    # After initiation, prices from Google kick in
    def __post_init__(self):  # self points to the object of type Coin
        price_info = get_price_info(self.coin_symbol, self.target_currency)

        # Only if logic is true, otherwise proceed with default values
        if price_info["coin_symbol"] == self.coin_symbol:
            self.usd_price = price_info["usd_price"]
            self.target_currency_price = price_info["target_currency_price"]

# Create a custom class for the Positions
@dataclass
class Position:
    coin: Coin # as previously defined
    quantity: float

# Create a custom class for the Portfolio
@dataclass
class Portfolio:
    positions: List[Position]

    def get_total_value(self):
        total_value = 0

        for position in self.positions:
            
            total_value += position.quantity * position.coin.target_currency_price
            
        return total_value

# Create a helper function to perform portfolio valuation
def display_portfolio_summary(portfolio):

    if not isinstance(portfolio, Portfolio):
        raise TypeError("Please provide an instance of the Portfolio type")

    portfolio_value = portfolio.get_total_value()

    position_data = []

    for position in sorted(portfolio.positions, key=lambda x: x.quantity * x.coin.target_currency_price,
                          reverse=True
                          ):
        
        position_data.append([
            position.coin.coin_symbol,
            position.quantity,
            position.coin.target_currency_price,
            position.quantity * position.coin.target_currency_price,
            position.quantity * position.coin.target_currency_price / portfolio_value * 100
        ])

    print(tabulate(position_data,
                   headers=["Coin",
                            "Holding",
                            "Price",
                            "Market Value",
                            "% Allocation"],
                   tablefmt="psql",
                   floatfmt=".2f"  
                  ))

    print(f"The total value of your portfolio at {hour}:{minute} on {now:%A}, {now:%d-%m-%Y} is {Coin.target_currency} {portfolio_value:,.2f}.")
    
if __name__ == "__main__":

    # Arbitrary user selected portfolio - amend as required
    bitcoin = Coin("bitcoin", "GBP")
    ethereum  = Coin("ethereum", "GBP")
    xrp = Coin("xrp", "GBP")

    positions = [Position(bitcoin, 1),
                 Position(ethereum, 1),
                 Position(xrp, 1)]    
      
    portfolio = Portfolio(positions)     
    
    display_portfolio_summary(portfolio)     
