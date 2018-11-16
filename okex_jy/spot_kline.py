#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#  kline 1分钟返回一次数据，每次返回两千行

from okex_jy.OkcoinSpotAPI import OKCoinSpot
import operator
import time
import os
import pandas as pd
import csv
import json
import sys
from threading import Thread
import datetime
from common.enums import *
from okex_xh.sender2 import MqSender
from config import config
from common.becash_funs import kline2db


class spot_kline_download(object):
    sym = ""
    def __init__(self, sym):
        # 获取OKCoin网址数据需要先注册一个账号，每个账号可以生成5组apikey和secretkey
        # 抽取数据的时候需要填写自己的apikey和secretkey
        # 每组apikey和secretkey可以在5分钟内提交3000次请求
        # OKCoin网址
        self.okcoinRESTURL = config.okcoinRESTURL
        self.sym = sym
    # 连接网址获取数据
    def download(self):
        sym = self.sym
        # 下载路径，可修改
        path = config.dir_path
        today_date = time.strftime("%Y%m%d")
        dir_path = '%s%s%s%s%s%s' % (path, today_date, os.sep, 'okex' , os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value)
        print(dir_path)
        # D:\data\20180817\kline
        txt_file_name = '%s%s%s_%s_%s.txt' % (dir_path, os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value, sym, today_date)
        csv_file_name = '%s%s%s_%s_%s.csv' % (dir_path, os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value ,sym, today_date)
        # 判断文件夹是否存在不存在则创建
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 现货API，连接
        okcoinSpot = OKCoinSpot(config.okcoinRESTURL, config.apikey, config.secretkey)
        # 获取当天凌晨零点零分13位时间戳
        today = datetime.date.today()
        ts = int(time.mktime(today.timetuple()) * 1000)
        rs_bch_usdt = okcoinSpot.kline(sym, ts)
        # 转换symbol
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
        # print(rs_bch_usdt)
        # 原始数据写入txt depth_20180724.txt
        # print(file_name)
        print(txt_file_name)
        print(csv_file_name)
        with open(txt_file_name, 'w', encoding='utf-8') as f:
            writer = f.write(json.dumps(rs_bch_usdt) + '\n')
        f.close()
        # 将格式化数据写入csv
        # 转化成json格式
        # print(rs_bch_usdt)
        # rr = json.dumps(rs_bch_usdt)
        # 调用小兵mq
        try:
            sender = MqSender('5', 'kline')
            sender.send(str(rs_bch_usdt+[symbol]))
        except Exception as e:
            print('MQ报错')

        with open(csv_file_name, 'w', encoding='utf-8', newline='') as f:
            heads = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol', 'count']
            writer = csv.writer(f)
            writer.writerow(heads)

            for i in rs_bch_usdt:
                result = {}
                result["symbol"] = symbol
                result["ts"] = i[0]
                result["tm_intv"] = "1m"
                result["id"] = i[0]
                result["open"] = i[1]
                result["close"] = i[4]
                result["low"] = i[3]
                result["high"] = i[2]
                result["amount"] = ""
                result["vol"] = i[5]
                result["count"] = ""
                writer.writerow(result.values())
                # 写入实时数据到Mongodb 用于becash
                kline2db(result, 'spot')
        f.close()

    # #循环
    # def loop(self):
    #     while True:
    #         try:
    #             rs_bch_usdt = self.download(OK.sym)
    #             time.sleep(59)
    #             print('ok')
    #         except Exception as e:
    #             print('掉了等5秒')
    #             time.sleep(5)


if __name__ == '__main__':
    spot_kline_download("btc_usdt").download()
    spot_kline_download("bch_usdt").download()
    spot_kline_download("eth_usdt").download()
    spot_kline_download("ltc_usdt").download()
    spot_kline_download("eos_usdt").download()








