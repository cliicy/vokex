#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#  kline 1分钟返回一次数据，每次返回两千行

from okex_jy.OkcoinFutureAPI import OKCoinFuture
import time
import os
import csv
import json
# import sys
# from threading import Thread
import datetime
from okex_xh.sender import MqSender
from common.enums import *
from config import config
from common.becash_funs import kline2db


class future_kline_download(object):
    sym = ""
    contractType = ""
    def __init__(self,sym,contractType):
        # 获取OKCoin网址数据需要先注册一个账号，每个账号可以生成5组apikey和secretkey
        # 抽取数据的时候需要填写自己的apikey和secretkey
        # 每组apikey和secretkey可以在5分钟内提交3000次请求
        # OKCoin网址
        self.okcoinRESTURL = config.okcoinRESTURL
        self.sym = sym
        self.contractType = contractType

    # 连接网址获取数据
    def download(self):
        sym = self.sym
        contractType = self.contractType
        # 下载路径，可修改 /yanjiuyuan/data/20180817/okex_future
        path = config.dir_path
        today_date = time.strftime("%Y%m%d")
        dir_path = '%s%s%s%s%s%s' % (
        path, today_date, os.sep, 'okex_future', os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value)
        # print(dir_path)
        # D:\data\20180817\kline
        txt_file_name = '%s%s%s_%s_%s_%s.txt' % (
        dir_path, os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value, sym,contractType, today_date)
        csv_file_name = '%s%s%s_%s_%s_%s.csv' % (
        dir_path, os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value, sym,contractType, today_date)

        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX_FUTURE, sym)
        # 昨天时间的文件夹
        # 今天日期
        today_j = datetime.date.today()
        # 昨天时间
        yesterday = str(today_j - datetime.timedelta(days=1)).replace('-', '')
        # 昨天开始时间戳
        yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y%m%d'))) * 1000
        dir_path_yesterday = '%s%s%s%s%s%s' % (
        path, yesterday, os.sep, 'okex_future', os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value)
        # print(dir_path_yesterday)
        # 昨天csv文件路径
        csv_file_name_yesterday = '%s%s%s_%s_%s_%s.csv' % (
            dir_path_yesterday, os.sep, PlatformDataType.PLATFORM_DATA_KLINE.value, sym, contractType, yesterday)
        # print(csv_file_name_yesterday)

        # 判断文件夹是否存在不存在则创建
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 期货API，连接
        okcoinFuture = OKCoinFuture(config.okcoinRESTURL, config.apikey, config.secretkey)
        # 获取当天凌晨零点零分13位时间戳
        today = datetime.date.today()
        ts = int(time.mktime(today.timetuple()) * 1000)

        # 转换成分钟 当天00:00
        ts_top = time.strftime('%Y-%m-%d %H', time.localtime(ts / 1000))
        # print(ts_top)
        # 现在分钟数
        ts_now = time.strftime('%Y-%m-%d %H', time.localtime(int(time.time())))
        # print(ts_now)
        if str(ts_top) == str(ts_now):
            # print(int(time.time()* 1000))
            f = open(csv_file_name_yesterday, 'r')
            content = csv.reader(f)
            lineNum = 0

            for line in content:
                lineNum += 1
            f.close()
            # print(lineNum)  # lineNum就是你要的文件行数
            if lineNum != 1441:
                rs_bch_usdt_yesterday = okcoinFuture.future_kline_bq(sym, contractType, yesterday_start_time)
                # 将格式化后的数据写入csv
                with open(csv_file_name_yesterday, 'w', encoding='utf-8', newline='') as f:
                    heads = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol',
                             'count', 'contractType']
                    writer = csv.writer(f)
                    writer.writerow(heads)
                    for i in rs_bch_usdt_yesterday[0:1440]:
                        result = {}
                        result['symbol'] = symbol
                        result['ts'] = i[0]
                        result['tm_intv'] = '1m'
                        result['id'] = i[0]
                        result['open'] = i[1]
                        result['close'] = i[4]
                        result['low'] = i[3]
                        result['high'] = i[2]
                        result['amount'] = ''
                        result['vol'] = i[6]
                        result['count'] = i[5]
                        result['contractType'] = contractType
                        writer.writerow(result.values())
                        # 写入实时数据到Mongodb 用于becash
                        kline2db(result, 'okex_future')
                f.close()

        rs_bch_usdt = okcoinFuture.future_kline(sym, contractType, ts)
        # print(rs_bch_usdt)
        # print(txt_file_name)
        # print(csv_file_name)
        # 原始数据写入txt depth_20180724.txt
        with open(txt_file_name, 'w', encoding='utf-8') as f:
            writer = f.write(json.dumps(rs_bch_usdt) + '\n')
        f.close()
        try:
            # 调用小兵mq
            sender = MqSender('4', 'kline')
            sender.send(str(rs_bch_usdt+[symbol]+[contractType]))
        except Exception as e:
            print('MQ报错')
        # 将格式化后的数据写入csv
        with open(csv_file_name, 'w', encoding='utf-8', newline='') as f:
            heads = ['symbol', 'ts', 'tm_intv', 'id', 'open', 'close', 'low', 'high', 'amount', 'vol',
                     'count', 'contractType']
            writer = csv.writer(f)
            writer.writerow(heads)
            for i in rs_bch_usdt:
                result = {}
                result['symbol'] = symbol
                result['ts'] = i[0]
                result['tm_intv'] = '1m'
                result['id'] = i[0]
                result['open'] = i[1]
                result['close'] = i[4]
                result['low'] = i[3]
                result['high'] = i[2]
                result['amount'] = ''
                result['vol'] = i[6]
                result['count'] = i[5]
                result['contractType'] = contractType
                writer.writerow(result.values())
                # 写入实时数据到Mongodb 用于becash
                kline2db(result, 'future')
        f.close()


if __name__ == '__main__':
    future_kline_download("btc_usd", "quarter").download()







