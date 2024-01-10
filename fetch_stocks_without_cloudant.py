from yahoo_fin import stock_info
import time
from datetime import datetime

def main(params):
    stocks = params['rows'][0]['doc']['equities']
    req_stocks = {}
    for stock in stocks:
        req_stocks[stock] = stock_info.get_live_price(stock)
        time.sleep(0.3)
    curtime = datetime.now().strftime('%H:%M')
    return {'_id': curtime, 'price':req_stocks}
    