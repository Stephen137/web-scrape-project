import requests as r
from bs4 import BeautifulSoup

# Fetch exchange rate
def fetch_exchange_rate(target_currency):
    fx_url = f"https://www.google.com/finance/quote/USD-{target_currency}"
    resp = r.get(fx_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    fx_rate = soup.find("div", attrs={"data-last-price": True})
    return float(fx_rate["data-last-price"])