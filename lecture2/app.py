from flask import Flask, render_template, Response
from urllib.parse import quote
import csv
from stock import Stock

app = Flask(__name__)

# stock list to show in website
stocks = []

# open stock_list.csv
# chinese in website -> encoding='utf-8'
with open('stock_list.csv', newline='', encoding='utf-8') as stock_csv:
    # take csv format turn to list
    temp = list(csv.reader(stock_csv))

    for t in temp:
        s = {'id': t[0], 'name': t[1]}
        stocks.append(s)


# home page route
@app.route('/')
def home():
    return render_template('home.html', stocks=stocks)


# stock pages route
@app.route('/stock/<stock_id>')
def stock_page(stock_id):
    # build stock instance
    stock = Stock(stock_id)
    # crawl stock infomation
    stock.fetch_data()
    # set stock data to web
    return render_template('stock.html', stock=stock)


if __name__ == '__main__':
    app.run(debug=True)
