# !-*-coding:utf-8 -*-
# @TIME    : 2018/6/11/0011 15:32
# @Author  : Nogo
import config.symbol as symbol
import subprocess
from multiprocessing import Process
from threading import Thread
def do_kline(sym, contractType):
    cmd = '{0}{1}{2}{3}'.format('python /root/yanyan/okex_investment/okex_jy/future_kline.py ', sym,' ',contractType)
    print(cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    #print(pipe.read())
    #print('finished to getting trades information')
class MarketApp(object):
    def __init__(self):
        self.c = []

    # 循环kline
    def loop_kline(self):
        # 循环调取depth
        for sy in symbol.f_symbol:
            for contractType in symbol.contractType:
                # self.do_trades(sy)
                print(sy, contractType)
                p = Process(target=do_kline, args=(sy, contractType,))
                print('syncing trades information will start.')
                p.start()

if __name__ == '__main__':
    run = MarketApp()
    kline = Thread(target=run.loop_kline)
    kline.start()
    kline.join()
    print('done')
