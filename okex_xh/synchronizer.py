#  -*- coding:utf-8 -*-
import okex_xh.websocket as websocket
import json
from okex_xh.sender import MqSender
import time
import os
from config import config
import zlib



class BaseSynchronizer(object):
    url = ''  # if okcoin.cn  change url wss://real.okcoin.cn:10440/websocket/okcoinapi
    data_type = ""
    platform = ""

    def __init__(self, platform, data_type, url):
        self.url = url
        self.data_type = data_type
        self.platform = platform

    def download(self, rdata):
        pass

    def save_csv(self, evt, txt_file_path, file_date, file_data_zh):
        pass

    def on_message(self, app, evt):
        # 将数据格式调整为字典格式
        # 用json转换成列表格式
        # print(evt)
        evt = self.inflate(evt)
        # 下面是自己的转换
        data = json.loads(evt)
        rdata = data[0]
        try:
            if rdata['channel'] == 'addChannel':
                pass
            else:
                # 调用mq
                sender = MqSender(self.platform, self.data_type)
                sender.send(evt)
        except Exception as e:
            print('MQ报错')
        self.download(rdata)

    def on_error(self, app, evt):
        print('raise ERROR')
        print(evt)

    def on_close(self, app):
        print('DISCONNECT')

    def on_open(self):
        pass

    def run(self):
        while True:
            host = self.url
            websocket.enableTrace(False)
            ws = websocket.WebSocketApp(host,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
            ws.on_open = self.on_open
            ws.run_forever()

    def download(self, evt):
        """
        获得返回值并写入文件
        :param evt:
        :return:
        """
        # 设置文件存放路径
        path = config.dir_path
        today_date = time.strftime("%Y%m%d")
        today_date_zh = time.strftime("%Y-%m-%d")
        txt_file_path = '%s%s%s%s%s' % (path, os.sep, today_date, os.sep, self.platform)
        # 判断文件是否存在
        if not os.path.exists(txt_file_path):
            print('创建文件夹')
            os.makedirs(txt_file_path)
        else:
            # 判断是否为需要数据
            if evt['channel'] == 'addChannel':
                pass
            else:
                # 将原始文件写入txt
                # 设置存储路径
                txt_file_name = '%s%s%s_%s.txt' % (txt_file_path, os.sep, self.data_type, today_date)
                csv_file_name = '%s%s%s_%s .csv' % (txt_file_path, os.sep, self.data_type, today_date)
                self.save_txt(evt, txt_file_name, today_date)

                self.save_csv(evt, csv_file_name, today_date, today_date_zh)

    def save_txt(self, evt, txt_file_name, file_date):
        """
        保存txt
        :param evt:数据
        :param txt_file_path:txt文件地址
        :param file_date:日期
        :return:
        """

        with open(txt_file_name, 'a+', encoding='utf-8') as f:
            writer = f.write(json.dumps(evt) + '\n')
        f.close()

    def inflate(self, data):
        decompress = zlib.decompressobj(
                - zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated