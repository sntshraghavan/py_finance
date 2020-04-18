"""IPython 3.1, Python 3.4, Windows 8.1"""
import pandas as pd
import urllib as u
import urllib.request
from bs4 import BeautifulSoup as bs

"""
First visit www.Finviz.com and get the base url for the quote page.
example: http://finviz.com/quote.ashx?t=aapl

Then write a simple function to retrieve the desired ratio. 
In this example I'm grabbing Price-to-Book (mrq) ratio
"""

def get_price2book( symbol ):
    try:
        url = r'http://finviz.com/quote.ashx?t={}'\
        				.format(symbol.lower())
        html = u.request.urlopen(url).read()
        soup = bs(html, 'lxml')
        # Change the text below to get a diff metric
        pb =  soup.find(text = r'P/B')
        pb_ = pb.find_next(class_='snapshot-td2').text
        roe =  soup.find(text = r'ROE')
        roe_ = roe.find_next(class_='snapshot-td2').text
        mc =  soup.find(text = r'Market Cap')
        mc_ = mc.find_next(class_='snapshot-td2').text
        de =  soup.find(text = r'Debt/Eq')
        de_ = de.find_next(class_='snapshot-td2').text
        dp =  soup.find(text = r'Dividend %')
        dp_ = dp.find_next(class_='snapshot-td2').text
        #print( '{} price to book = {} '.format(symbol, pb_) )
        #print( '{} roe = {} '.format(symbol, roe_) )
        return (pb_,roe_,mc_,de_,dp_)
    except Exception as e:
        print(e)
        
"""
Construct a pandas series whose index is the list/array
of stock symbols of interest.

Run a loop assigning the function output to the series
"""
#stock_list = ['XOM','MMM']
#p2b_series = pd.Series( index=stock_list )
#
#for sym in stock_list:
#	p2b_series[sym] = get_price2book(sym)
#print(p2b_series)
#print(p2b_series['MMM'][0])
