import ccxt
import pandas as pd


def get_tokens_from_trading_pairs(trading_pairs):
    return list(set([token for pair in trading_pairs for token in pair.split("-")]))


def hbot_trading_pairs_to_ccxt_trading_pairs(trading_pairs):
    return [pair.replace("-", "/") for pair in trading_pairs]


def get_exchange(exchange_id, api_key, api_secret):
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': api_key,
        'secret': api_secret,
    })
    exchange.load_markets()
    return exchange


def get_balances(exchange, trading_pairs):
    tokens = get_tokens_from_trading_pairs(trading_pairs)
    balances = {token: balance for token, balance in exchange.fetch_balance()["total"].items() if balance > 0}
    return {token: balances.get(token, 0) for token in tokens}


def get_trades(exchange, trading_pairs, start_time, end_time):
    trading_pairs = hbot_trading_pairs_to_ccxt_trading_pairs(trading_pairs)
    start_time_ts = exchange.parse8601(start_time)
    end_time_ts = exchange.parse8601(end_time)
    trades = []
    for trading_pair in trading_pairs:
        initial_time = start_time_ts
        while initial_time < end_time_ts:
            new_trades = exchange.fetch_my_trades(symbol=trading_pair, since=initial_time)
            if len(new_trades):
                last_trade = new_trades[len(trades) - 1]
                initial_time = last_trade['timestamp'] + 1
            else:
                initial_time += 432000000  # 5 days
            trades = trades + new_trades
    return pd.DataFrame([trade["info"] for trade in trades])
