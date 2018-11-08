# -*- coding: utf-8 -*-
import okex_xh.websocket as websocket
from gevent import monkey
from okex_jy.future_kline import future_kline_download
monkey.patch_all()
import gevent
import time

def run_task():
    # symbol = ['btc_usd','bch_usd','eth_usd','ltc_usd','eos_usd']
    # contractType = ['this_week','next_week','quarter']
    try:
        greenlets = [
            gevent.spawn(future_kline_download("btc_usd", "this_week").download()),
            gevent.spawn(future_kline_download("bch_usd", "this_week").download()),
            gevent.spawn(future_kline_download("eth_usd", "this_week").download()),
            gevent.spawn(future_kline_download("ltc_usd", "this_week").download()),
            gevent.spawn(future_kline_download("eos_usd", "this_week").download()),
            gevent.spawn(future_kline_download("btc_usd", "next_week").download()),
            gevent.spawn(future_kline_download("bch_usd", "next_week").download()),
            gevent.spawn(future_kline_download("eth_usd", "next_week").download()),
            gevent.spawn(future_kline_download("ltc_usd", "next_week").download()),
            gevent.spawn(future_kline_download("eos_usd", "next_week").download()),
            gevent.spawn(future_kline_download("btc_usd", "quarter").download()),
            gevent.spawn(future_kline_download("bch_usd", "quarter").download()),
            gevent.spawn(future_kline_download("eth_usd", "quarter").download()),
            gevent.spawn(future_kline_download("ltc_usd", "quarter").download()),
            gevent.spawn(future_kline_download("eos_usd", "quarter").download())
        ]
        gevent.joinall(greenlets)
    except Exception as e:
        print(e)
# 循环
def start():
    while True:
        try:
            run_task()
            time.sleep(30)
            print('ok')
        except Exception as e:
            print('掉了等5秒')
            time.sleep(5)

if __name__ == '__main__':
    start()

