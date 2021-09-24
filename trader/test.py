import json
import re
import time
import pandas as pd
import requests
import numpy as np
from lxml import etree
import lxml.html as LH
from bs4 import BeautifulSoup

def read_csv(path='code.csv'):
    data = np.loadtxt(path, dtype=str, delimiter=',', encoding='utf-8')
    return data

def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

def get_online_data():
    header = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    }

    r = requests.get(url="http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-09-24&ed=2021-09-24&qdii=&tabSubtype=,,,,,&pi=3&pn=50&dx=1&v=0.9687047682263124", headers=header)
    print(r.text)
# def get_jingzhi():
#     headers = {
#         "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
#     }
#     for j in range(1, 49):
#         url = 'http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s6yzf;pn50;ddesc;qsd20200924;qed20210924;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb0'
#         resp = requests.get(url, headers=headers).text
#         print(resp)
#         str_ = resp[102:]
#         list1 = eval(str_.split(",count")[0])
#         print(f'正在爬取第{j}页')
#         print(f'本页爬取{len(list1)}条数据')
#         num = []
#         name = []
#         today_price = []
#         yesterday_price = []
#         day_value = []
#         day_value_rate = []
#         subscription_status = []
#         redemption_status = []
#         service_charge = []
#
#
#         for i in range(len(list1)):
#           # 1、基金代码号
#             num.append(list1[i][0])
#             # 2、股票名称
#             name.append(list1[i][1])
#       # 3、今日基金净额
#             today_price.append(list1[i][3])
#             # 4、昨日基金净额
#             yesterday_price.append(list1[i][5])
#             # 5、日增长值
#             day_value.append(list1[i][7])
#             # 6、日增长率
#             day_value_rate.append(list1[i][8])
#             # 7、申购状态
#             subscription_status.append(list1[i][9])
#             # 8、赎回状态
#             redemption_status.append(list1[i][10])
#             # 9、手续费
#             service_charge.append(list1[i][17])
#
#
#         df = pd.DataFrame()
#         df['基金代码'] = num
#         df['基金名称'] = name
#         df['2020-08-12\n单位净值'] = today_price
#         df['2020-08-11\n单位净值'] = yesterday_price
#         df['日增长值'] = day_value
#         df['日增长率\n%'] = day_value_rate
#         df['申购状态'] = subscription_status
#         df['赎回状态'] = redemption_status
#         df['手续费'] = service_charge
#
#
#         try:
#             df.to_excel(f'基金{j}.xlsx', '基金信息', index=None, encoding='utf-8')
#             continue
#
#
#         except Exception as e:
#             print(e)
#
#
#     time.sleep(1)

if __name__ == '__main__':
    get_online_data()
    # data = read_csv()
    # # http://fund.eastmoney.com/pingzhongdata/%160216.js
    # for dd in data:
    #     code = dd[0]
    #     # fcode, fname, fgz, fzzl = get_jingzhi(code)
    #     # print(fcode, fname, fgz, fzzl)