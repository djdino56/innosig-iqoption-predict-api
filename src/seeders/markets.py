from binance.enums import KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_3MINUTE, KLINE_INTERVAL_5MINUTE, \
    KLINE_INTERVAL_15MINUTE, KLINE_INTERVAL_30MINUTE
from database.models.market import Market


def create(market: dict):
    market = Market(**market)
    market.save()
    print(market)


def main():
    markets = [
        {
            "market": "BTCUSDT",
            "interval": KLINE_INTERVAL_1MINUTE
        },
        {
            "market": "BTCUSDT",
            "interval": KLINE_INTERVAL_3MINUTE
        },
        {
            "market": "BTCUSDT",
            "interval": KLINE_INTERVAL_5MINUTE
        },
        {
            "market": "BTCUSDT",
            "interval": KLINE_INTERVAL_15MINUTE
        },
        {
            "market": "BTCUSDT",
            "interval": KLINE_INTERVAL_30MINUTE
        },
    ]
    for market in markets:
        create(market)


if __name__ == '__main__':
    main()
