import time
import threading
from okex_jy.OkcoinSpotAPI import OKCoinSpot

apikey = '0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec'
secretkey = '82B69BD2B7DBBABF726D046C37C7969F'
okcoinRESTURL = 'www.okex.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn



def chaxun(symbol):
    # #现货API
    time_start = time.time()
    okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)
    print(threading.currentThread())
    okcoinSpot.orderinfo(symbol, '-1')
    time_end = time.time()
    print('未提取耗时：', time_end - time_start)
def diaoyong():
    for i in range(10):
        new_thread_1 = threading.Thread(target=chaxun,args=('eos_usdt',))
        new_thread_2 = threading.Thread(target=chaxun, args=('eos_usdt',))
        new_thread_3 = threading.Thread(target=chaxun, args=('eos_usdt',))
        new_thread_4 = threading.Thread(target=chaxun, args=('eos_usdt',))
        new_thread_5 = threading.Thread(target=chaxun, args=('eos_usdt',))
        new_thread_1.start()
        new_thread_2.start()
        new_thread_3.start()
        new_thread_4.start()
        new_thread_5.start()

if __name__ == '__main__':
    a = diaoyong()
