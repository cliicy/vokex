# -*- coding: utf-8 -*-
import okex_xh.websocket as websocket
from gevent import monkey
from okex_xh.okex_webs_depth import *
from okex_xh.okex_webs_trades import *
from okex_xh.okex_webs_ticker import *
from okex_xh.okex_web_future_trades import *
from okex_xh.okex_web_future_ticker import *
from okex_xh.okex_web_future_depth import *
monkey.patch_all()
import gevent


def run_task():
    try:
        greenlets = [
            gevent.spawn(OkexDepthSynchronizer().run()),
            gevent.spawn(OkexTradesSynchronizer().run()),
            gevent.spawn(OkextickerSynchronizer.run()),
            gevent.spawn(OkexFutureTradesSynchronizer().run()),
            gevent.spawn(OkexFutureTickerSynchronizer.run()),
            gevent.spawn(OkexFutureDepthSynchronizer().run())
        ]
        gevent.joinall(greenlets)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_task()
