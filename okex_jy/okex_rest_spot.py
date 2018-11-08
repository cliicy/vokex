# !-*-coding:utf-8 -*-
# @TIME    : 2018/6/11/0011 15:32
# @Author  : Nogo
import config.symbol as symbol
import subprocess
from multiprocessing import Process
from threading import Thread

#开进程调用kline
def do_kline(sym):
    cmd = '{0}{1}'.format('python /root/yanyan/okex_investment/okex_jy/spot_kline.py ', sym)
    print(cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print('finished to getting trades information')
class MarketApp(object):
    def __init__(self):
        self.c = []
    # 循环kline
    def loop_kline(self):
        # 循环调取depth
        for sy in symbol.symbol:
            # self.do_trades(sy)
            print(sy)
            p = Process(target=do_kline, args=(sy,))
            print('syncing kline information will start.')
            p.start()
if __name__ == '__main__':
    run = MarketApp()
    kline = Thread(target=run.loop_kline)
    kline.start()
    kline.join()
    print('done')
