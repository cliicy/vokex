from config.settings import future_kline_coll, dwM1_coll, ticker_coll


def ticker2db(result, exchange, interval_type):
    # 写入实时数据到Mongodb 用于becash
    # 把 下面的实时数据写入 Mongodb中
    # 'latest_price' 最新成交价
    # pre_24h_price_max 24小时内最高价
    # pre_24h_price_min 24小时内最低价
    # pre_24h_usd_finish_amt 24小时内计价货币成交量
    # 现货指数    Index
    # 持仓量    Holding
    # 24小时最高    24h High
    # 24小时成交量  24h Vol
    # 24小时最低    24h Low
    # okex合约： {'binary': 1, 'channel': 'ok_sub_futureusd_eos_ticker_next_week', 'data': {
    #     'high': '5.1itLow': '4.303', 'vol': '7071258', 'last': '4.426', 'low': '3.973', 'buy': '4.426',
    #  'hold_amount':, 'sell': '4.431', 'contractId': 201811230200053, 'unitAmount': '10',
    # 'limitHigh': '4.574'}}
    # 货币对
    ybdd = {}
    ybdd['interval_type'] = interval_type
    ybdd['sym'] = result['symbol']
    ybdd['Index'] = result['limitHigh']
    ybdd['Holding'] = result['hold_amount']
    # 价格 Price  latest_price
    ybdd['Price'] = result['latest_price']
    # 涨跌幅 Change 需要自己计算 或从网页爬取
    # delta = '0.11'
    pre_pp = '({}-{})/{}*100'.format(result['latest_price'], result['pre_24h_price'],
                                     result['pre_24h_price'])
    ff = eval(pre_pp)
    print(ff)
    delta = ('%.2f' % ff)
    ybdd['Change'] = '{0}{1}'.format(delta, '%')

    ybdd['exchange'] = exchange
    ybdd['api'] = 'ticker'
    # Volume pre_24h_usd_finish_amt 24小时内计价货币成交量
    if exchange == 'future':
        # High  pre_24h_price_max 24小时内最高价
        ybdd['24h High'] = result['pre_24h_price_max']
        # Low pre_24h_price_min 24小时内最低价
        ybdd['24h Low'] = ['pre_24h_price_min']
        ybdd['24h Vol'] = round(result['volume_24h'], 2)
        #现货指数
    elif exchange == 'okex_spot':
        # 人民币价格
        # 24h最高价 24h成交量 24h最低价
        # High  pre_24h_price_max 24小时内最高价
        ybdd['24h High'] = result['high']
        # Low pre_24h_price_min 24小时内最低价
        ybdd['24h Low'] = ['low']
        ybdd['Change'] = result['change']
        ybdd['24h Vol'] = round(result['vol'], 2)
    ticker_coll.update({'sym': ybdd['sym']}, {'$set': {'Price': ybdd['Price'], 'Change': ybdd['Change'],
                                                       'High': ybdd['High'], 'Low': ybdd['Low'],
                                                       'Volume': ybdd['Volume'], 'exchange': ybdd['exchange'],
                                                       'api': 'ticker', 'interval_type': ybdd['interval_type']}}, True)


def kline2db(ddict, exchange):
    # 写入实时数据到Mongodb 用于becash
    ybdd = {}
    ybdd['exchange'] = exchange
    ybdd['sym'] = ddict["symbol"]
    ybdd['info_name'] = 'kline'
    # 开盘价格
    ybdd['open'] = ddict['open']
    # 最高价格
    ybdd['high'] = ddict['high']
    # 最低价
    ybdd['low'] = ddict['low']
    # close
    ybdd['close'] = ddict['close']
    # count
    ybdd['count'] = ddict['count']
    # quote_vol 计价货币成交量
    ybdd['quote_vol'] = round(ddict['vol'], 2)
    ybdd['_id'] = '{0}_{1}_{2}'.format(ddict['id'], ddict['seq'], ddict['quote_vol'])
    if exchange == 'future':
        # 间隔时间
        ybdd['interval'] = ddict['contractType']
        future_kline_coll.insert(ybdd)
    elif exchange == 'spot':
        # 间隔时间
        ybdd['interval'] = ddict['tm_intv']
        dwM1_coll.insert(ybdd)


