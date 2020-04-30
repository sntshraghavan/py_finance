import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


#def save_dow_tickers():
#    resp = requests.get('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
#    soup = bs.BeautifulSoup(resp.text, 'lxml')
#    table = soup.find('table', {'class': 'wikitable sortable'})
#    tickers = []
#    for row in table.findAll('tr')[1:]:
#        ticker = row.findAll('td')[0].text
#        tickers.append(ticker)
#    with open("sp500tickers.pickle", "wb") as f:
#        pickle.dump(tickers, f)
#    return tickers

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        print(ticker)
        tickers.append(ticker)
    tickers.append("spy ")
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
        #print(tickers)
        #tickers = save_dow_tickers()
        #print(tickers)
	
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    #start = dt.datetime(2019, 1, 1)
    #end = dt.date.today() #datetime(2020, 4, 18)
    start = dt.datetime(2019, 1, 1)
    end = dt.date.today() #datetime(2020, 4, 18)
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        ticker = ticker[:-1]
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            print(ticker+" downloading") 
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            #df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))




#    analysis = pd.DataFrame(columns=['tick', 'ratio'],index=range(0,500) )
#            #df['10ma']=(df['Adj Close'].rolling(window=10, min_periods=0).mean())
#            #print(df.shape)
#            #print(df['10ma'].iloc[1])
#            print(df['10ma'].iloc[320]/df['10ma'].iloc[1])
#            analysis.loc[i] =  [ticker  ,  df['10ma'].iloc[320]/df['10ma'].iloc[1] ]
#            print(analysis)

#save_sp500_tickers()
get_data_from_yahoo()



