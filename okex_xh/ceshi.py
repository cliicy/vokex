import time
import re
# 1534237740000.00
# 1534237800000.00
# data = {'ts':'1534237740000'}
# x = int(data['ts']) + 60000
# print(x)
# 1534243200198 和 1534243200205  我查的怎么2个时间换算成北京时间 是一样的
# 2018-08-14 18:40:00
# 2018-08-14 18:40:00
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(1534243200205/1000)))
# # import os
# # path = 'D:\\YANYAN\\okex_rest\\kline_eth_usdt_20180814_config.txt'
# # print(os.path.getsize(path))
#
# a= "ok_sub_futureusd_btc_ticker_this_week"
# symbol = re.match('.*_future(.*)_ticker.*', a).group(1)
# print(symbol)
# ss = '_'.join(symbol.split('_')[::-1])
# print(ss)

a = 'bid' # bid

c = 'sell' if a == 'ask' else 'buy'

print(c)