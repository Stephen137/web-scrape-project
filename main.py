# Import required libraries
from price_fetcher import Coin, Position, Portfolio
from portfolio_val import display_portfolio_summary

if __name__ == "__main__":
    # Arbitrary user-selected portfolio
    bitcoin = Coin("bitcoin", "GBP")
    ethereum = Coin("ethereum", "GBP")
    xrp = Coin("xrp", "GBP")

    positions = [
        Position(bitcoin, 1),
        Position(ethereum, 1),
        Position(xrp, 1)
    ]

    portfolio = Portfolio(positions)
    display_portfolio_summary(portfolio)