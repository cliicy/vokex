# -*- coding: utf-8 -*-
import okex_xh.websocket as websocket
from gevent import monkey
from okex_jy.spot_kline import spot_kline_download
monkey.patch_all()
import gevent
import time

def run_task():
    # symbol = ['btc_usdt','bch_usdt','eth_usdt','ltc_usdt','eos_usdt','eth_btc','eos_btc']
    try:
        greenlets = [
            gevent.spawn(spot_kline_download("btc_usdt").download()),
            gevent.spawn(spot_kline_download("bch_usdt").download()),
            gevent.spawn(spot_kline_download("eth_usdt").download()),
            gevent.spawn(spot_kline_download("ltc_usdt").download()),
            gevent.spawn(spot_kline_download("eos_usdt").download()),
            gevent.spawn(spot_kline_download("xrp_usdt").download()),
            gevent.spawn(spot_kline_download("eth_btc").download()),
            gevent.spawn(spot_kline_download("eos_btc").download())
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

