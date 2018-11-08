#  -*- coding:utf-8 -*-
from common.enums import PlatformDataType, Platform
import os
import csv
import operator
from okex_xh.synchronizer import BaseSynchronizer
from common.enums import *
from config.config import websocket_spot_compress_url

class OkextickerSynchronizer(BaseSynchronizer):
    """
    okex depth 数据同步器
    """

    def __init__(self):
        self.platform = Platform.PLATFORM_OKEX.value
        self.data_type = PlatformDataType.PLATFORM_DATA_TICKER.value
        self.url = websocket_spot_compress_url
        BaseSynchronizer(self.platform, self.data_type, self.url)

    def on_open(app, self):
        # subscribe okcoin.com spot ticker
        self.send("[{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_bch_usdt_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eth_usdt_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_ltc_usdt_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eos_usdt_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_xrp_usdt_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eth_btc_ticker'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eos_btc_ticker'}"
                  "]")

    def save_csv(self, evt, file_name, file_date, file_date_zh):
        """
        保存csv
        :param evt:数据
        :param txt_file_path:txt文件地址
        :param file_date:日期
        :param file_date_zh:格式化日期
        :return:
        """
        headers = {'symbol', 'ts', 'latest_price', 'latest_amount', 'max_buy1_price', 'max_buy1_amt', 'min_sell1_price',
                   'min_sell1_amt', 'pre_24h_price', 'pre_24h_price_max', 'pre_24h_price_min', 'pre_24h_bt_finish_amt',
                   'pre_24h_usd_finish_amt'}
        # 内容
        # 解析获得文件的格式
        result = {}
        sym = '_'.join(evt['channel'].split('_')[3:5])
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
        result['symbol'] = symbol
        result['ts'] = evt['data']['timestamp']
        result['latest_price'] = evt['data']['last']
        result['latest_amount'] = ''
        result['max_buy1_price'] = evt['data']['buy']
        result['max_buy1_amt'] = ''
        result['min_sell1_price'] = evt['data']['sell']
        result['min_sell1_amt'] = ''
        result['pre_24h_price'] = ''
        result['pre_24h_price_max'] = evt['data']['high']
        result['pre_24h_price_min'] = evt['data']['low']
        result['pre_24h_bt_finish_amt'] = evt['data']['vol']
        result['pre_24h_usd_finish_amt'] = ''
        print(result)
        # 判断文件是否存在，如果存在则直接写入数据，如果不存在则创建文件
        if os.path.exists(file_name):
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(result.values())
            f.close()
        else:
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(result.keys())
                writer.writerow(result.values())
            f.close()
# OkextickerSynchronizer-------
if __name__ == '__main__':
    OkextickerSynchronizer().run()

