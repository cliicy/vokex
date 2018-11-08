# -*- coding: utf-8 -*-
import operator
import re
from common.enums import PlatformDataType, Platform
import os
import csv
from okex_xh.synchronizer import BaseSynchronizer
from common.enums import *
from config.config import websocket_future_compress_url

class OkexFutureDepthSynchronizer(BaseSynchronizer):
    """
    okex future trade 数据同步器
    """

    def __init__(self):
        self.platform = Platform.PLATFORM_OKEX_FUTURE.value
        self.data_type = PlatformDataType.PLATFORM_DATA_DEPTH.value
        self.url = websocket_future_compress_url
        BaseSynchronizer(self.platform, self.data_type ,self.url)

    def on_open(app, self):
        # subscribe okcoin.com spot ticker
        self.send("[{'event':'addChannel','channel':'ok_sub_futureusd_btc_depth_this_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_depth_this_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eth_depth_this_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_etc_depth_this_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_bch_depth_this_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_depth_this_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_depth_next_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_depth_next_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eth_depth_next_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_etc_depth_next_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_bch_depth_next_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_depth_next_week_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_depth_quarter_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_depth_quarter_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eth_depth_quarter_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_etc_depth_quarter_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_bch_depth_quarter_20'},"
                  "{'event':'addChannel','channel':'ok_sub_futureusd_eos_depth_quarter_20'},"
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
        # 头部
        headers = ['symbol', 'contractType', 'ts', 'depth', 'sell_price', 'sell_amt', 'sell_amt_cont', 'sell_count_amt',
                   'sell_count_amt_cont', 'buy_price', 'buy_amt', 'buy_amt_cont', 'buy_count_amt',
                   'buy_count_amt_cont', ]
        # 内容
        # 解析获得文件的格式
        sym = re.match('.*_future(.*)_depth.*', evt['channel']).group(1)
        symbol_get = '_'.join(sym.split('_')[::-1])

        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX_FUTURE, symbol_get)
        contractType = re.match('.*_depth_(.*)_20', evt['channel']).group(1)

        ts = evt['data']['timestamp']
        # 卖方深度 先排序 reverse=False 升序
        rs_eos_usdt_asks_1 = sorted(evt['data']['asks'], key=operator.itemgetter(0), reverse=False)
        rs_eos_usdt_asks = [[symbol] + [ts] + [i + 1] + value for i, value in enumerate(rs_eos_usdt_asks_1)]
        # 买方深度
        rs_eos_usdt_bids = evt['data']['bids']
        # 设置数据存放列表
        result = []
        # 设置存储路径
        # 判断文件是否存在，如果存在则直接写入数据，如果不存在则创建文件
        if os.path.exists(file_name):
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                for i in range(len(rs_eos_usdt_asks)):
                    item1 = rs_eos_usdt_asks[i]
                    item2 = rs_eos_usdt_bids[i]
                    item3 = item1 + item2
                    temp = [item3[0], contractType, item3[1], item3[2], item3[3], item3[5], item3[4], item3[6],
                            item3[7], item3[8], item3[10], item3[9], item3[11], item3[12]]
                    result.append(temp)
                    # print(result)
                    # print('11111111111111111111111111111')
                for csv_i in result:
                    # print(file_name)
                    writer = csv.writer(f)
                    writer.writerow(csv_i)
            f.close()
        else:
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for i in range(len(rs_eos_usdt_bids)):
                    item1 = rs_eos_usdt_asks[i]
                    item2 = rs_eos_usdt_bids[i]
                    item3 = item1 + item2
                    temp = [item3[0], contractType, item3[1], item3[2], item3[3], item3[5], item3[4], item3[6],
                            item3[7],
                            item3[8], item3[10], item3[9], item3[11], item3[12]]
                    result.append(temp)
                for csv_i in result:
                    # print(file_name)
                    writer.writerow(csv_i)
            f.close()
# OkexFutureTradesSynchronizer结束-------
if __name__ == '__main__':
    OkexFutureDepthSynchronizer().run()