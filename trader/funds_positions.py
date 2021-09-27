from urllib import request
from bs4 import BeautifulSoup
import re
import pymysql
import requests

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
    print(r.text)


def main():
    funds = []
    fund_ids = []
    fundNum = 0
    errorNum = 0
    send = request.Request(url="http://fund.eastmoney.com/js/fundcode_search.js", headers=head)
    response = request.urlopen(send)
    js = response.read().decode('utf-8')
    list1 = js[11:-2].split('],[')
    for i in range(len(list1)):
        fund = str(list1[i]).replace('"', '')
        fund = fund.split(',')
        fund_ids.append(fund[0])
        funds.append(fund)

    for i in range(len(fund_ids)):
        url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=2021&month=&rt=0.21822537857648627" \
            .format(fund_ids[i])
        get_data(url)

    # while fundNum < len(fund_ids):
    #

    #     send = request.Request(url, headers=head)
    #     response = request.urlopen(send, timeout=1)
    #     html = response.read().decode('utf-8')
    #     bs = BeautifulSoup(html, 'html.parser')
    #     find_list = bs.find_all("tbody")
    #     if find_list != []:
    #         tr = find_list[0].find_all("tr")
    #         print(tr)
    #     fundNum += 1


if __name__ == "__main__":
    main()