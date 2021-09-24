import requests
import re

class Eastmoney(object):
    def __init__(self):
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        }
        self._session = requests.session()
        self._session.headers = self.headers
        self.fund_url = "http://fund.eastmoney.com/data/rankhandler.aspx"
        self.fund_archives_url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"

    def set_start_end_date(self, start, end):
        self.params['sd'] = start
        self.params['ed'] = end

    def get_fund_count(self):

        self.params = {
            'op': 'ph',
            'dt': 'kf',
            'ft': 'all',
            'rs': '',
            'gs': 0,
            'sc': 'zzf',
            'st': 'desc',
            'sd': '2019-01-12',
            'ed': '2020-01-12',
            'qdii': '',
            'tabSubtype': ',,,,,',
            'pi': 1,
            'pn': 50,
            'dx': 1,
            'v': '0.7637284533252435'
        }
        try:
            r = self._session.get(self.fund_url, headers=self.headers, params=self.params)
            pattern = r'allNum:(\d+)'
            allNum = re.search(pattern, r.text).groups()
            return allNum[0]
        except Exception as e:
            print('get fund count error', e)
            return None

    def get_fund_code(self):
        all_num = self.get_fund_count()
        if not all_num:
            all_num = 10000
        self.params['pn'] = all_num



