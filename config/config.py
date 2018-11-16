#  -*- coding:utf-8 -*-
import os
dir_path = '/yanjiuyuan/data' if os.environ.get("SHELL", "") else 'data\\'
# dir_path = '/yanjiuyuan/data/'
okcoinRESTURL = 'www.okex.com'
apikey = '29567657-bf7e-4934-a397-14eb4bae4be6'
secretkey = '841E084D176E39749F25AD15E890041B'

websocket_future_compress_url = "wss://real.okex.com:10440/websocket/okexapi?compress=true"
websocket_spot_compress_url = "wss://real.okex.com:10441/websocket?compress=true"

