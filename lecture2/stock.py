from urllib.request import urlopen
from pyquery import PyQuery


class Stock:
    # Stock contains following attributes
    # Stock id,name, deal price, buy price, sell price
    def __init__(self, sid):
        self.id = sid
        self.name = None
        self.price = None
        self.bid = None
        self.offer = None

    # define a function to crawl Stock's information
    # crawl target : https://tw.stock.yahoo.com/q/q?s=2330
    def fetch_data(self):
        # crawl the target website
        page = urlopen('https://tw.stock.yahoo.com/q/q?s=' + self.id)
        # use big5 decode
        raw_html = page.read().decode('big5')
        # sent raw_html to pyquery
        html = PyQuery(raw_html)
        data = html('td[align="center"]').text().split()
        self.name = data[0][4:]
        self.price = data[3]
        self.bid = data[4]
        self.offer = data[5]