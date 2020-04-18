import time
import urllib2
from urllib2 import urlopen

def yahooKeyStats(stock):
    try:
        sourceCode = urllib2.urlopen('http://finance.yahoo.com/q/ks?s='+stock).read()
        pbr = sourceCode.split('Price/Book (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        print('price to book ratio:',stock,pbr)

    except Exception:
        print('failed in the main loop')
		
yahooKeyStats('MMM')
