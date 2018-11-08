import time
from okex_jy.OkcoinSpotAPI import OKCoinSpot
apikey = '0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec'
secretkey = '82B69BD2B7DBBABF726D046C37C7969F'
okcoinRESTURL = 'www.okex.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn

# #现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
time_start = time.time()
for i in range(100):
    okcoinSpot.orderinfo('eos_usdt', '-1')

time_end = time.time()
print('未提取耗时：', time_end - time_start)
