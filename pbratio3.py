import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials



yahoo_financials = YahooFinancials('MMM')
print(yahoo_financials.get_key_statistics_data())



#assets = ['TSLA', 'MSFT', 'FB']
#
#yahoo_financials = YahooFinancials('BTC-USD')
#
##data = yahoo_financials.get_summary_data()
#data = yahoo_financials.get_key_statistics_data()
##get_historical_price_data(start_date='2019-01-01',
##                                                  end_date='2019-12-31',
##                                                  time_interval='weekly')
##
##prices_df = pd.DataFrame({
##    a: {x['formatted_date']: x['adjclose'] for x in data[a]['prices']} for a in assets
##})
#print(data)
