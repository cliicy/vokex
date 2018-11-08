#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

from okex_jy.OkcoinSpotAPI import OKCoinSpot
from okex_jy.OkcoinFutureAPI import OKCoinFuture
import time

#初始化apikey，secretkey,url
#apikey = 'XXXX'
#secretkey = 'XXXXX'
apikey = '0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec'
secretkey = '82B69BD2B7DBBABF726D046C37C7969F'
okcoinRESTURL = 'www.okex.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn

# #现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

# 期货API
okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)

# print (u' 现货行情 ')
# print (okcoinSpot.ticker('btc_usdt'))

# print (u' 现货深度 ')
# print (okcoinSpot.depth('btc_usd'))

# print (u' 现货历史交易信息 ')
# print (okcoinSpot.trades('btc_usd'))

# print (u' kline信息 ')
# print (okcoinSpot.kline('eos_btc'))

# print (u' 用户现货账户信息 ')
# print (okcoinSpot.userinfo())

# print (u' 现货下单 ')
# print (okcoinSpot.trade('eos_usdt','buy','7.0607','1'))

#print (u' 现货批量下单 ')
#print (okcoinSpot.batchTrade('ltc_usd','buy','[{price:0.1,amount:0.2},{price:0.1,amount:0.2}]'))

# print (u' 现货取消订单 ')
# print (okcoinSpot.cancelOrder('eos_usdt','739298602'))

# print (u' 现货订单信息查询 ')
# print (okcoinSpot.orderinfo('eos_usdt','-1'))
#
# print (u' 现货批量订单信息查询 ')
# print (okcoinSpot.ordersinfo('ltc_usd','18243800,18243801,18243644','0'))

# print (u' 现货历史订单信息查询 ')
# print (okcoinSpot.orderHistory('eos_usdt','1','1','1'))

# print (u' 期货行情信息')
# print (okcoinFuture.future_ticker('btc_usdt','this_week'))

# print (u' 期货市场深度信息')
# print (okcoinFuture.future_depth('btc_usd','this_week','20'))

# print (u'期货交易记录信息')
# print (okcoinFuture.future_trades('ltc_usd','this_week'))

# print (u'期货指数信息')
# print (okcoinFuture.future_index('eos_usdt'))

#print (u'美元人民币汇率')
#print (okcoinFuture.exchange_rate())

#print (u'获取预估交割价') 
#print (okcoinFuture.future_estimated_price('ltc_usd'))

# print (u'获取全仓账户信息')
# print (okcoinFuture.future_userinfo())

#print (u'获取全仓持仓信息')
#print (okcoinFuture.future_position('ltc_usd','this_week'))

# print (u'期货下单')
# print (okcoinFuture.future_trade('eos_usdt','this_week','5.523','1','4','0','10'))

#print (u'期货批量下单')
#print (okcoinFuture.future_batchTrade('ltc_usd','this_week','[{price:0.1,amount:1,type:1,match_price:0},{price:0.1,amount:3,type:1,match_price:0}]','20'))

# print (u'期货取消订单')
# print (okcoinFuture.future_cancel('eos_usd','this_week',"1248113571947520"))

# print (u'期货获取订单信息')
# print (okcoinFuture.future_orderinfo('eos_usd','this_week','-1','1','1','1'))

# print (u'期货获取详细订单信息')
# print (okcoinFuture.future_ordersinfo('eos_usd','this_week','-1'))

#print (u'期货逐仓账户信息')
#print (okcoinFuture.future_userinfo_4fix())

#print (u'期货逐仓持仓信息')
# #print (okcoinFuture.future_position_4fix('ltc_usd','this_week',1))
#
# print (u'个人账户资金划转')#7.22219450 --  8.15469450
# print('开始划转%s' %time.time())
# print (okcoinFuture.future_devolve('eos','1','0.1'))
# print('划转结束%s' %time.time())

# print(okcoinFuture.future_kline('bch_usdt','quarter', '1534345140000'))

print (u' kline信息 ')
print (okcoinSpot.kline('bch_usdt','1534345140000'))
