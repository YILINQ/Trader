from urllib import request
from bs4 import BeautifulSoup
import re
import pymysql
import requests
from requests_html import HTMLSession
import time
import pandas


session = HTMLSession()
fundShareList = []

head = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    "Referer": "http://fund.eastmoney.com/data/fundranking.html",
}


find = {
    1: re.compile(r'html">(.*?)</a></td>'),
    2: re.compile(r'html">(.*?)</a></td>'),
    6: re.compile(r'">(.*?)</a></td>'),
    7: re.compile(r'">(.*?)</a></td>'),
    8: re.compile(r'">(.*?)</a></td>')
}

def handle(a):
    flag = False
    for i in range(0, len(fundShareList)):
        if a[0] == fundShareList[i][0]:
            fundShareList[i][2] = round(float(fundShareList[i][2])) + float(a[4], 2)
            flag = True
            break
    if not flag:
        new = [a[0], a[1], a[4]]
        fundShareList.append(new)

def get_data(url):
    r = requests.get(url=url, headers=head)
    return(r.text)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches



def main():
    funds = []
    fund_ids = []
    fundNum = 0
    send = request.Request(url="http://fund.eastmoney.com/js/fundcode_search.js", headers=head)
    response = request.urlopen(send)
    js = response.read().decode('utf-8')
    list1 = js[11:-2].split('],[')
    for i in range(len(list1)):
        fund = str(list1[i]).replace('"', '')
        fund = fund.split(',')
        fund_ids.append(fund[0])
        funds.append(fund)
    fund_counter = 0

    while fundNum < len(fund_ids) and fund_counter < 30:
        fund_id = funds[fundNum][0]
        try:
            stock_codes = []
            stock_names = []
            price_value_percent = []
            stock_position_num = []
            stock_position_value = []




            url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=" + str(fund_id) + "&topline=10&year=2021&month=&rt=0.21822537857648627"
            send = request.Request(url,headers = head)
            response = request.urlopen(send, timeout=10)
            html = response.read().decode('utf-8')
            bs =BeautifulSoup(html,"html.parser")

            find_list = bs.find_all("tbody")


            if find_list != []:
                tr = find_list[0].find_all("tr")
                for i in tr:
                    td = i.find_all("td")
                    l = str(td)

                    name_results = re.findall('html">(.*?)</a></td>', l)

                    price_results = re.findall('<td class="tor">(.*?)</td>', l)
                    # name_results[0] == stock_code
                    # name_results[1] == stock_name
                    # price_results[-3] == 占净值比
                    # price_results[-2] == 持股数
                    # price_results[-1] == 持仓市值
                    stock_codes.append(name_results[0])
                    stock_names.append(name_results[1])
                    price_value_percent.append(price_results[-3])
                    stock_position_num.append(price_results[-2])
                    stock_position_value.append(price_results[-1])

                df = pandas.DataFrame()
                df['股票代码'] = stock_codes
                df['股票名称'] = stock_names
                df['占净值比'] = price_value_percent
                df['持股数(万)'] = stock_position_num
                df['持仓市值'] = stock_position_value


                df.to_excel(f'{fund_id}_{funds[fundNum][2]}.xlsx', 'stock_position_info', index=None, encoding='utf-8')
                fund_counter += 1

        except:
            print(fund_id + " 获取失败")
        fundNum += 1


if __name__ == "__main__":
    main()