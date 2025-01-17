from tabulate import tabulate
import datetime as dt

# Get the current timestamp
def get_current_timestamp():
    now = dt.datetime.now()
    return now, now.hour, now.minute

# Display the portfolio summary
def display_portfolio_summary(portfolio):
    now, hour, minute = get_current_timestamp()
    portfolio_value = portfolio.get_total_value()

    position_data = [
        [
            position.coin.coin_symbol,
            position.quantity,
            position.coin.target_currency_price,
            position.quantity * position.coin.target_currency_price,
            position.quantity * position.coin.target_currency_price / portfolio_value * 100,
        ]
        for position in sorted(
            portfolio.positions, key=lambda x: x.quantity * x.coin.target_currency_price, reverse=True
        )
    ]

    print(
        tabulate(
            position_data,
            headers=["Coin", "Holding", "Price", "Market Value", "% Allocation"],
            tablefmt="psql",
            floatfmt=".2f",
        )
    )

    print(
        f"The total value of your portfolio at {hour}:{minute} on {now:%A}, {now:%d-%m-%Y} is "
        f"{portfolio.positions[0].coin.target_currency} {portfolio_value:,.2f}."
    )
 