import json
import re
import time
import pandas as pd
import requests
import numpy as np
from lxml import etree
import lxml.html as LH
from bs4 import BeautifulSoup

FUND_CODE = 0
FUND_NAME = 1
FUND_danweijingzhi = 4
FUND_leijijingzhi = 5
FUND_DAY_INCREASE = 6
FUND_WEEK_INCREASE = 7
FUND_MONTH_INCREASE = 8
FUND_QUATER_INCREASE = 9
FUND_HALF_YEAR_INCREASE = 10
FUND_ONE_YEAR_INCREASE = 11
FUND_TWO_YEAR_INCREASE = 12
FUND_THREE_YEAR_INCREASE = 13
FUND_THIS_YEAR_INCREASE = 14
FUND_INCREASE_SINCE_FOUND = 15

def read_csv(path='code.csv'):
    data = np.loadtxt(path, dtype=str, delimiter=',', encoding='utf-8')
    return data

def convert_text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

def get_online_data():
    header = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    "Referer": "http://fund.eastmoney.com/data/fundranking.html",
    }
    for j in range(1, 49):
        # url = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-09-24&ed=2021-09-24&qdii=&tabSubtype=,,,,,&pi={j}&pn=50&dx=1&v=0.9687047682263124'
        r = requests.get(url="http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-09-25&ed=2021-09-25&qdii=&tabSubtype=,,,,,&pi={}&pn=50&dx=1&v=0.9687047682263124".format(j), headers=header)

        funds = r.text[r.text.find('[')+1:]
        funds = funds[:funds.index(']')+1]
        # [(.*?)\]

        str_ = funds.split(",")
        list1 = []
        for n in range(50):
            list1.append(str_[n*25 : (n+1)*25])
        num = []
        name = []
        today_price = []
        today_increase_rate = []
        for i in range(len(list1)):
            num.append(list1[i][FUND_CODE][1:])
            name.append(list1[i][FUND_NAME])
            today_price.append(list1[i][FUND_danweijingzhi])
            today_increase_rate.append(list1[i][FUND_DAY_INCREASE])
        df = pd.DataFrame()
        df['基金代码'] = num
        df['基金名称'] = name
        df['单位净值'] = today_price
        df['日增长率'] = today_increase_rate
        try:
            print("generating fund list {}".format(j))
            df.to_excel(f'fundlist_{j}.xlsx', 'fund_info', index=None, encoding='utf-8')

        except Exception as e:
            print(e)

if __name__ == '__main__':
    get_online_data()