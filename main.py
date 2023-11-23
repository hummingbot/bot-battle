# The dates are in UTC
from utils import get_balances, get_exchange, get_trades

COMPETITION_START_DATE = "2023-11-01T00:00:00"
COMPETITION_END_DATE = "2023-11-22T00:00:00"

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

for user, data in USERS_DATA.items():
    try:
        exchange = get_exchange(data["exchange_id"], data["api_key"], data["api_secret"])
    except Exception as e:
        print(f"Failed to get exchange for {user}: {e}")
        continue
    balances = get_balances(exchange, data["trading_pairs"])
    prices = get_prices(exchange, data["trading_pairs"])
    initial_balance_usdt = sum([balance * prices[f"{token}-USDT"] for token, balance in balances.items() if token != "USDT"]) + balances.get("USDT", 0)
    trades = get_trades(exchange, data["trading_pairs"], COMPETITION_START_DATE, COMPETITION_END_DATE)
    trades["initial_balance_usdt"] = initial_balance_usdt
    trades.to_csv(f"data/{user}.csv")