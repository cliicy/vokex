import json

path_config = 'D:\\YANYAN\\data\\20180814\\okex\\kline_btc_usdt_config.txt'

with open(path_config, 'r', encoding='utf-8') as f:
    for a in f:
        print(a)
        data = eval(a)
        print(data)
f.close()
with open(path_config, 'w', encoding='utf-8') as f1:
    if data['symbol'] == 'btc_usdt':
        data['ts'] = 'bbbbbb'
    print(data)
    f1.write(str(data))
f1.close()