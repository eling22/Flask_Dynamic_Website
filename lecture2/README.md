# Day2 Flask-Dynamic-Router-Pactice
This is the second day, I learn flask.
today, we combine web crawler to show stock information on a dynamic website.

First step, make a stock_list.csv .

	1101,台泥
	2303,聯電
	2317,鴻海
	2330,台積電
	2393,億光
	2412,中華電
	2324,仁寶
	2454,聯發科
	2891,中信金
	3045,台灣大
	3231,緯創
	3481,群創

and then let data in csv turn to dict.

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

## crawl stock data

you could make a class first. and then make a function crawl data.  
`urlopen` could crawl data from URL.  
`decode('big5')` could let you see chinese words.  
`PyQuery` could help you to search what you want to focus.
if you want to focus on `<td align="center" ...]...</td>`, you can use `data = html('td[align="center"]')` and you can get all of them.


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
## use Bootstrap
go to [bootstrap's getting start](https://getbootstrap.com/docs/4.3/getting-started/introduction/), copy the css `<link>` into your `<head>`.

	<head>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <meta http-equiv="X-UA-Compatible" content="ie=edge">
	    <title>Stock Information Search</title>
	    <!-- use Bootstrap.css -->
	    <!-- https://getbootstrap.com/ -->
	    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
	        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	</head>

