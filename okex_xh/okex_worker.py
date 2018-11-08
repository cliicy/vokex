# -*- coding: utf-8 -*-
import okex_xh.websocket as websocket
from gevent import monkey
from okex_xh.okex_webs_depth import *
from okex_xh.okex_webs_trades import *
from okex_xh.okex_webs_ticker import *
from okex_xh.okex_web_future_trades import *
from okex_xh.okex_web_future_ticker import *
from okex_xh.okex_web_future_depth import *
from okex_jy.spot_kline import spot_kline_download
from okex_jy.future_kline import future_kline_download
monkey.patch_all()
import gevent


def run_task():
    try:
        greenlets = [
            gevent.spawn(OkexDepthSynchronizer().run),
            gevent.spawn(OkexTradesSynchronizer().run),
            gevent.spawn(OkextickerSynchronizer().run),
            gevent.spawn(OkexFutureTickerSynchronizer().run),
            gevent.spawn(OkexFutureTradesSynchronizer().run),
            gevent.spawn(OkexFutureDepthSynchronizer().run),
            # gevent.spawn(spot_kline_download("btc_usdt").download()),
            # gevent.spawn(spot_kline_download("bch_usdt").download()),
            # gevent.spawn(spot_kline_download("eth_usdt").download()),
            # gevent.spawn(spot_kline_download("ltc_usdt").download()),
            # gevent.spawn(spot_kline_download("eos_usdt").download()),
            # gevent.spawn(spot_kline_download("xrp_usdt").download()),
            # gevent.spawn(spot_kline_download("eth_btc").download()),
            # gevent.spawn(spot_kline_download("eos_btc").download()),
            # gevent.spawn(future_kline_download("btc_usd", "this_week").download()),
            # gevent.spawn(future_kline_download("bch_usd", "this_week").download()),
            # gevent.spawn(future_kline_download("eth_usd", "this_week").download()),
            # gevent.spawn(future_kline_download("ltc_usd", "this_week").download()),
            # gevent.spawn(future_kline_download("eos_usd", "this_week").download()),
            # gevent.spawn(future_kline_download("btc_usd", "next_week").download()),
            # gevent.spawn(future_kline_download("bch_usd", "next_week").download()),
            # gevent.spawn(future_kline_download("eth_usd", "next_week").download()),
            # gevent.spawn(future_kline_download("ltc_usd", "next_week").download()),
            # gevent.spawn(future_kline_download("eos_usd", "next_week").download()),
            # gevent.spawn(future_kline_download("btc_usd", "quarter").download()),
            # gevent.spawn(future_kline_download("bch_usd", "quarter").download()),
            # gevent.spawn(future_kline_download("eth_usd", "quarter").download()),
            # gevent.spawn(future_kline_download("ltc_usd", "quarter").download()),
            # gevent.spawn(future_kline_download("eos_usd", "quarter").download()),
        ]
        gevent.joinall(greenlets)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_task()
    # while True:
    #     try:
    #         run_task()
    #     except Exception as e:
    #         time.sleep(1)
