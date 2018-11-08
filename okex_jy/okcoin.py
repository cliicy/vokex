# !-*-coding:utf-8 -*-
# @TIME    : 2018/6/11/0011 15:32
# @Author  : Nogo
import python.config.symbol as symbol
import subprocess
from multiprocessing import Process
from threading import Thread

#开进程调用trade
def do_trades(sym):
    cmd = '{0}{1}'.format('python /root/yanyan/rest/python/trade.py ', sym)
    print(cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    #print(pipe.read())
    #print('finished to getting trades information')
#开进程调用kline
def do_kline(sym):
    cmd = '{0}{1}'.format('python /root/yanyan/rest/python/kline.py ', sym)
    print(cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    #print(pipe.read())
    #print('finished to getting trades information')
#开进程调用kline
def do_depth(sym):
    cmd = '{0}{1}'.format('python /root/yanyan/rest/python/depth.py ', sym)
    print(cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    #print(pipe.read())
    #print('finished to getting trades information')
#开进程调用ticker
def do_ticker(sym):
    cmd = '{0}{1}'.format('python /root/yanyan/rest/python/ticker.py ', sym)
    print(cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    #print(pipe.read())
    #print('finished to getting trades information')
class MarketApp(object):
    def __init__(self):
        self.c = []

    # 循环trades
    def loop_trades(self):
        #循环调取trades
        for sy in symbol.symbol:
            # self.do_trades(sy)
            print(sy)
            p = Process(target=do_trades, args=(sy,))
            print('syncing trades information will start.')
            p.start()

    # 循环kline
    def loop_kline(self):
        # 循环调取depth
        for sy in symbol.symbol:
            # self.do_trades(sy)
            print(sy)
            p = Process(target=do_kline, args=(sy,))
            print('syncing kline information will start.')
            p.start()
    # 循环depth
    def loop_depth(self):
        # 循环调取depth
        for sy in symbol.symbol:
            # self.do_trades(sy)
            print(sy)
            p = Process(target=do_depth, args=(sy,))
            print('syncing kline information will start.')
            p.start()
    # 循环kline
    def loop_ticker(self):
        # 循环调取depth
        for sy in symbol.symbol:
            # self.do_trades(sy)
            print(sy)
            p = Process(target=do_ticker, args=(sy,))
            print('syncing kline information will start.')
            p.start()
if __name__ == '__main__':
    run = MarketApp()
    trades = Thread(target=run.loop_trades)
    kline = Thread(target=run.loop_kline)
    depth = Thread(target=run.loop_depth)
    ticker = Thread(target=run.loop_ticker)
    trades.start()
    kline.start()
    depth.start()
    ticker.start()
    trades.join()
    kline.join()
    depth.join()
    ticker.join()
    print('done')
