#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 现货行情

from python.OkcoinSpotAPI import OKCoinSpot
import operator
import time
import os
import csv
import json
import sys
from threading import Thread

class OK_download(object):
    def __init__(self):
        # 获取OKCoin网址数据需要先注册一个账号，每个账号可以生成5组apikey和secretkey
        # 抽取数据的时候需要填写自己的apikey和secretkey
        # 每组apikey和secretkey可以在5分钟内提交3000次请求
        self.apikey = '29567657-bf7e-4934-a397-14eb4bae4be6'
        self.secretkey = '841E084D176E39749F25AD15E890041B'

        # OKCoin网址
        self.okcoinRESTURL = 'www.okex.com'

        # 下载路径，可修改
        self.path = 'D:\\YANYAN\\data\\'

        # 时间
        self.today_date = time.strftime("%Y%m%d")
        self.stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        # 文件夹第一层 /data/20180723
        self.path_file = self.path + self.today_date
        # 文件夹第二层 /data/20180723/okex
        self.path_txt = self.path_file + '\\okex'
    #创建文件夹
    def create_file(self):
        if not os.path.exists(self.path_txt):
            os.makedirs(self.path_txt)





    # 连接网址获取数据
    def download(self,sym):
        # 现货API，连接
        okcoinSpot = OKCoinSpot(self.okcoinRESTURL, self.apikey, self.secretkey)
        # 期货API，连接
        # okcoinFuture = OKCoinFuture(self.okcoinRESTURL, self.apikey, self.secretkey)
        print(u' 现货行情 '+str(self.stime))
        # 需要传递参数币种：bch_usdt\bch_usdt\eth_usd\etc_usd\bch_usd
        rs_json = okcoinSpot.ticker(sym)
        #原始数据写入txt depth_20180724.txt
        #判断文件夹是否存在
        self.create_file()
        path = self.path_txt + '\\ticker_'+ sym +'_'+ self.today_date + '.txt'
        with open(path , 'a+', encoding='utf-8') as f:
            writer = f.write(json.dumps(rs_json)+'\n')
        f.close()
        #解析获得文件的格式
        #print('bch_usdt')
        result = {}
        result['symbol'] = sym
        result['ts']=rs_json['date']+'000'
        result['latest_price'] = rs_json['ticker']['last']
        result['latest_amount'] = ''
        result['max_buy1_price'] = rs_json['ticker']['buy']
        result['max_buy1_amt'] = ''
        result['min_sell1_price'] = rs_json['ticker']['sell']
        result['min_sell1_amt'] = ''
        result['pre_24h_price'] = ''
        result['pre_24h_price_max'] = rs_json['ticker']['high']
        result['pre_24h_price_min'] = rs_json['ticker']['low']
        result['pre_24h_bt_finish_amt'] = rs_json['ticker']['vol']
        result['pre_24h_usd_finish_amt'] = ''



        return result

    # 每天创建一个csv
    def create_exccl(self):
        #获取数据
        rs_bch_usdt = self.download(OK.sym)
        #获取爬取时间
        #t = [str(self.stime)]
        # 设置存储路径
        file_name = self.path_txt + '\\ticker_'+ OK.sym +'_'+ self.today_date + '.csv'
        #判断文件是否存在，如果存在则直接写入数据，如果不存在则创建文件
        if os.path.exists(file_name):
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(rs_bch_usdt.values())
            f.close()
        else:
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(rs_bch_usdt.keys())
                writer.writerow(rs_bch_usdt.values())
            f.close()
            # 现货深度卖出结束-------
    #循环
    def loop(self):
        while True:
            try:
                rs_bch_usdt = self.create_exccl()
                print('ok')
            except Exception as e:
                print('掉了等5秒')
                time.sleep(5)
if __name__ == '__main__':
    OK = OK_download()
    OK.sym = sys.argv[1]
    thread = Thread(target=OK.loop)
    thread.start()
    thread.join()
    print('done')

