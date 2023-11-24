# The dates are in UTC
import time

import pandas as pd

from utils import get_balances, get_exchange, get_trades, get_prices

COMPETITION_START_DATE = "2023-11-24T00:00:00"
COMPETITION_END_DATE = "2023-11-27T00:00:00"

USERS_DATA = {
    "user1": {
        "trading_pairs": ["BLUR-USDT", "ETH-USDT"],
        "exchange_id": "binanceusdm",
        "api_key": "api_key",
        "api_secret": "api_secret",
    },
    "user2": {
        "trading_pairs": ["BLUR-USDT", "ETH-USDT"],
        "exchange_id": "binanceusdm",
        "api_key": "api_key",
        "api_secret": "api_secret",
    },
}

user_balances = {}
query_time = time.time()
for user, data in USERS_DATA.items():
    try:
        exchange = get_exchange(data["exchange_id"], data["api_key"], data["api_secret"])
    except Exception as e:
        print(f"Failed to get exchange for {user}: {e}")
        continue
    balances = get_balances(exchange, data["trading_pairs"])
    prices = get_prices(exchange, data["trading_pairs"])
    initial_balance_usdt = sum([balance * prices[f"{token}-USDT"] for token, balance in balances.items() if token != "USDT"]) + balances.get("USDT", 0)
    user_balances[user] = {
        "timestamp": query_time,
        "balances": balances,
        "prices": prices,
        "initial_balance_usdt": initial_balance_usdt,
    }
    trades = get_trades(exchange, data["trading_pairs"], COMPETITION_START_DATE, COMPETITION_END_DATE)
    trades.to_csv(f"data/{user}.csv")
user_balances_df = pd.DataFrame(user_balances).T
user_balances_df.to_csv(f"data/user_balances_{query_time}.csv")