#!/usr/bin/env python3

from datetime import datetime, timedelta
from iexfinance.stocks import get_historical_data
import requests_cache


def extract_first_close(data=dict):
    """
    Extract the closing price of the first trading day of each month
    Input is ordered dict
    """
    dates = []
    prices = []
    prev_month = ""
    for key in data.keys():
        year, month, day = key.split("-")
        if month != prev_month:
            price = data[key]["close"]
            prices.append(price)
            dates.append(key)
            #print("{}\t{}".format(key, price))
        prev_month = month
    return dates, prices


start = datetime(2013, 12, 1)
today = datetime.today()

expiry = timedelta(days=3)
session = requests_cache.CachedSession(
    cache_name="cache", backend="sqlite", expire_after=expiry
)

all_dates = []
all_prices = []
for i, symbol in enumerate(["IVV", "IXUS", "SHY"]):
    data = get_historical_data(symbol, start, today, session=session)
    d, p = extract_first_close(data)
    all_dates.append(d)
    all_prices.append(p)

assert len(all_dates[0]) == len(all_dates[1]) == len(all_dates[2])

result = [
    "{},{},{},{}".format(day, usa, intl, bond)
    for day, usa, intl, bond in zip(
        all_dates[0], all_prices[0], all_prices[1], all_prices[2]
    )
]
print("date,IVV,IXUS,SHY")
print("\n".join(result))
