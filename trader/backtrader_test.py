# -*- coding:utf-8 -*-

import backtrader as bt

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000.0)

print('starting')
cerebro.run()
print('final value: %.2f'% cerebro.broker.get_value())

