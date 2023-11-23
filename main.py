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
    exchange = get_exchange(data["exchange_id"], data["api_key"], data["api_secret"])
    balances = get_balances(exchange, data["trading_pairs"])
    print(f"{user} balances: {balances}")
    trades = get_trades(exchange, data["trading_pairs"], COMPETITION_START_DATE, COMPETITION_END_DATE)
    print(f"{user} trades: {trades}")