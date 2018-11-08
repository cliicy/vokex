import time
from okex_jy.OkcoinFutureAPI import OKCoinFuture
apikey = '0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec'
secretkey = '82B69BD2B7DBBABF726D046C37C7969F'
okcoinRESTURL = 'www.okex.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn

# 期货API
okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)
time_start = time.time()
for i in range(100):
    # time_start = time.time()
    # print(time_start)
    # print(u'期货获取订单信息')
    # print(okexFuture.get_order(Symbol.EOS_USDT, 'this_week', '-1', '2', '1', '2'))
    okcoinFuture.future_orderinfo('eos_usd','this_week','-1','2','1','2')
    # time.sleep(1)
    # print('---------')

time_end = time.time()
print('未提取耗时：', time_end - time_start)
