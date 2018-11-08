#  -*- coding:utf-8 -*-
from common.enums import PlatformDataType, Platform
import os
import csv
import operator
from okex_xh.synchronizer import BaseSynchronizer
from common.enums import *
from config.config import websocket_spot_compress_url


class OkexDepthSynchronizer(BaseSynchronizer):
    """
    okex depth 数据同步器
    """

    def __init__(self):
        self.platform = Platform.PLATFORM_OKEX.value
        self.data_type = PlatformDataType.PLATFORM_DATA_DEPTH.value
        self.url = websocket_spot_compress_url
        BaseSynchronizer(self.platform, self.data_type, self.url)

    def on_open(app, self):
        # subscribe okcoin.com spot ticker
        self.send("[{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_bch_usdt_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eth_usdt_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_ltc_usdt_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eos_usdt_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_xrp_usdt_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eth_btc_depth_20'},"
                  "{'event':'addChannel','channel':'ok_sub_spot_eos_btc_depth_20'}"
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
        headers = ['symbol', 'ts', 'depth', 'sell_price', 'sell_amt', 'buy_price', 'buy_amt']
        # 内容
        # 解析获得文件的格式
        sym = '_'.join(evt['channel'].split('_')[3:5])
        symbol = Symbol.convert_to_standard_symbol(Platform.PLATFORM_OKEX, sym)
        ts = evt['data']['timestamp']
        # 卖方深度
        rs_eos_usdt_asks_1 = sorted(evt['data']['asks'], key=operator.itemgetter(0), reverse=False)
        rs_eos_usdt_asks = [[symbol] + [ts] + [i + 1] + value for i, value in enumerate(rs_eos_usdt_asks_1)]
        # 买方深度
        rs_eos_usdt_bids = evt['data']['bids']
        # 设置数据存放列表
        result = []

        # 判断文件是否存在，如果存在则直接写入数据，如果不存在则创建文件
        if os.path.exists(file_name):
            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                for i in range(len(rs_eos_usdt_asks)):
                    item1 = rs_eos_usdt_asks[i]
                    item2 = rs_eos_usdt_bids[i]
                    temp = item1 + item2
                    result.append(temp)
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
                    temp = item1 + item2
                    result.append(temp)
                for csv_i in result:
                    # print(file_name)
                    writer.writerow(csv_i)
            f.close()
# OkexDepthSynchronizer结束-------
if __name__ == '__main__':
    OkexDepthSynchronizer().run()