# -*- coding: utf-8 -*-
import okex_xh.websocket as websocket
import time
import json
import os
import csv
import pandas as pd
from okex_xh.sender import MqSender
import re
import zlib

# 创建文件夹
def create_file(self):
    if not os.path.exists(self.path_txt):
        os.makedirs(self.path_txt)


def on_open(self):
    # subscribe okcoin.com spot ticker
    # self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_this_week_1min'}")
    self.send("[{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_this_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_this_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_this_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_etc_kline_this_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_this_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_this_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_next_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_next_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_next_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_etc_kline_next_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_next_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_next_week_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_etc_kline_quarter_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_1min'},"
              "{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_1min'},"
              "]")


# 获得返回值并写入文件
def download(self, evt, result):
    # 设置文件存放路径
    path = 'D:\\data_future\\'
    today_date = time.strftime("%Y%m%d")
    path_txt = path + today_date + '\\okex'
    # 判断文件是否存在
    if not os.path.exists(path_txt):
        print('创建文件夹')
        os.makedirs(path_txt)
    else:
        # 判断是否为需要数据
        if evt['channel'] == 'addChannel':
            pass
        else:
            # 将原始文件写入txt
            ok_path = path_txt + '\\kline_' + today_date + '.txt'
            with open(ok_path, 'a+', encoding='utf-8') as f:
                writer = f.write(json.dumps(evt) + '\n')
            f.close()
            # 调整数据格式存入csv
            # 头部
            if evt['channel'] == 'addChannel':
                pass
            else:
                # 获得币种 合约类型
                symbol = re.match('.*_future(.*)_kline.*', evt['channel']).group(1) + re.match('.*_kline_(.*)_1min',
                                                                                               evt['channel']).group(1)
                # print(symbol)
                # 获得合约类型
                # contractType = re.match('.*_kline_(.*)_1min', evt['channel']).group(1)
                # 将当前获得的数据放入列表
                a = evt['data']
                i = a[0]
                line = [re.match('.*_future(.*)_kline.*', evt['channel']).group(1),
                        re.match('.*_kline_(.*)_1min', evt['channel']).group(1),
                        i[0], '1m', i[0], i[1], i[4], i[3], i[2], '', i[6], i[5]]
                # 如果 dict 为空 则插入
                if not result:  # {}
                    result[symbol] = line
                if symbol not in result:
                    result[symbol] = line
                else:
                    # 如果symbol 在 dict 中 比较 新来的数据 id 与字典中的 id是否相同 相同则更新字典中的key，如果不同的话 将字典中的key数据 写入到CSV，最新的数据更新字典中的key，继续比较。
                    if ''.join(line[0:2]) == ''.join(result[symbol][0:2]) and line[2] == result[symbol][2]:
                        # print('1------------------------------1')
                        result[symbol] = line
                    else:
                        # print('2------------------------------1')
                        file_name = path_txt + '\\kline_' + today_date + '.csv'
                        if os.path.exists(file_name):
                            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow(result[symbol])
                            f.close()
                        else:
                            # print('3------------------------------1')
                            with open(file_name, 'a+', encoding='utf-8', newline='') as f:
                                writer = csv.writer(f)
                                header = ['symbol', 'contractType', 'ts', 'tm_intv', 'id', 'open', 'close', 'low',
                                          'hight', 'amount',
                                          'vol',
                                          'count']
                                writer.writerow(header)
                                writer.writerow(result[symbol])
                            f.close()
                    result[symbol] = line

                    # 现货深度卖出结束-------


def on_message(self, evt):
    # 将数据格式调整为字典格式
    # 用json转换成列表格式
    # print(evt)
    evt = inflate(evt)
    data = json.loads(evt)
    rdata = data[0]
    if rdata['channel'] == 'addChannel':
        pass
    else:
        # 调用小兵mq
        sender = MqSender('okcoin_future', 'kline')
        sender.send(evt)
    download(self, rdata, result)


def inflate(data):
    decompress = zlib.decompressobj(
        - zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def on_error(self, evt):
    print('7777777777777777777')
    print(evt)


def on_close(self):
    print('DISCONNECT')


if __name__ == "__main__":
    from config.config import websocket_future_compress_url

    while True:
        url = websocket_future_compress_url  # if okcoin.cn  change url wss://real.okcoin.cn:10440/websocket/okcoinapi
        api_key = '0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec'
        secret_key = '82B69BD2B7DBBABF726D046C37C7969F'
        # 存放上一条数据
        result = {}
        host = url
        websocket.enableTrace(False)
        # if len(sys.argv) < 2:
        #     host = url
        # else:
        #     host = sys.argv[1]
        ws = websocket.WebSocketApp(host,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
