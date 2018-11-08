#  -*- coding:utf-8 -*-
import time
from common.enums import PlatformDataType, Platform
import os
import csv
from okex_xh.synchronizer import BaseSynchronizer
from common.enums import *
from config.config import websocket_spot_compress_url


class OkexTradesSynchronizer(BaseSynchronizer):
    """
    okex depth 数据同步器
    """

    def __init__(self):
        self.platform = Platform.PLATFORM_OKEX.value
        self.data_type = PlatformDataType.PLATFORM_DATA_TRADE.value
        self.url = websocket_spot_compress_url
        BaseSynchronizer(self.platform, self.data_type, self.url)

    def on_open(app, self):
        # subscribe okcoin.com spot ticker
        self.send("[{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_bch_usdt_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eth_usdt_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_ltc_usdt_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eos_usdt_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_xrp_usdt_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eth_btc_deals'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eos_btc_deals'}"
                  "]")

    def save_csv(self, evt, file_name, file_date, file_date_zh):
        """
        保存csv
        :param evt:数据
        :param txt_file_path:txt文件地址
        :param file_date:日期
        :return:
        """
        # 调整数据格式存入csv
        # 判断文件是否存在，如果存在则直接写入数据，如果不存在则创建文件
        if os.path.exists(file_name):
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                # 存放数据
                result = {}
                data = evt['data']
                for i in data:
                    # print(i)
                    sym = '_'.join(evt['channel'].split('_')[3:5])
                    symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
                    result['symbol'] = symbol
                    result['id'] = i[0]
                    result['ts'] = int(
                        time.mktime(time.strptime(file_date_zh + ' ' + i[3], '%Y-%m-%d %H:%M:%S'))) * 1000
                    result['direction'] = 'sell' if i[4] == 'ask' else 'buy'
                    result['amount'] = i[2]
                    result['price'] = i[1]
                    writer = csv.writer(f)
                    writer.writerow(result.values())
            f.close()
        else:
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                headers = ['symbol', 'id', 'ts', 'direction', 'amount', 'price']
                writer.writerow(headers)
                # 存放数据
                result = {}
                data = evt['data']
                for i in data:
                    # print(i)
                    sym = '_'.join(evt['channel'].split('_')[3:5])
                    symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
                    result['symbol'] = symbol
                    result['id'] = i[0]
                    result['ts'] = int(
                        time.mktime(time.strptime(file_date_zh + ' ' + i[3], '%Y-%m-%d %H:%M:%S'))) * 1000
                    result['direction'] = 'sell' if i[4] == 'ask' else 'buy'
                    result['amount'] = i[2]
                    result['price'] = i[1]
                    writer.writerow(result.values())
            f.close()
# OkexTradeSynchronizer结束-------
if __name__ == '__main__':
    OkexTradesSynchronizer().run()