# -*- coding: utf-8 -*-
import time
import re
from common.enums import PlatformDataType, Platform
import os
import csv
from okex_xh.synchronizer import BaseSynchronizer
from common.enums import *
from config.config import websocket_future_compress_url


class OkexFutureTickerSynchronizer(BaseSynchronizer):
    """
    okex future trade 数据同步器
    """

    def __init__(self):
        self.platform = Platform.PLATFORM_OKEX_FUTURE.value
        self.data_type = PlatformDataType.PLATFORM_DATA_TICKER.value
        self.url = websocket_future_compress_url
        BaseSynchronizer(self.platform, self.data_type, self.url)

    def on_open(app, self):
        # subscribe okcoin.com spot ticker
        self.send("[{'event':'addChannel','channel':'ok_sub_futureusd_btc_ticker_this_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_ticker_this_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eth_ticker_this_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_etc_ticker_this_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_bch_ticker_this_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_ticker_this_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_ticker_next_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_ticker_next_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eth_ticker_next_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_etc_ticker_next_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_bch_ticker_next_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_ticker_next_week'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_ticker_quarter'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_ticker_quarter'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eth_ticker_quarter'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_etc_ticker_quarter'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_bch_ticker_quarter'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_ticker_quarter'},"
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
        # 调整数据格式存入csv
        # 内容
        # 解析获得文件的格式
        result = {}
        sym = re.match('.*_future(.*)_ticker.*', evt['channel']).group(1)
        symbol_get = '_'.join(sym.split('_')[::-1])

        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX_FUTURE, symbol_get)
        result['symbol'] = symbol
        result['ts'] = int(time.time() * 1000)
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
        result['limitHigh'] = evt['data']['limitHigh']
        result['limitLow'] = evt['data']['limitLow']
        result['unitAmount'] = evt['data']['unitAmount']
        result['hold_amount'] = evt['data']['hold_amount']
        result['contractId'] = evt['data']['contractId']
        result['contractType'] = re.match('.*_ticker_(.*)', evt['channel']).group(1)
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


# OkexFutureTradesSynchronizer结束-------
if __name__ == '__main__':
    OkexFutureTickerSynchronizer().run()
