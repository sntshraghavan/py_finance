import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import pbratio4 


def analyse_data_from_yahoo():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    analysis = pd.DataFrame(columns=['drop ratio','pb','roe','market cap','price on 04-09','Debt/Eq','Dividend %'])
    #analysis = pd.DataFrame(columns=['tick', 'ratio'])
    i=0
    for ticker in tickers:
        i=i+1
        #print(df.shape)
        ticker = ticker[:-1]
        if os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), parse_dates=True, index_col=0)
            #print(ticker,df.shape,df.shape[0] )
            df['10ma']=(df['Adj Close'].rolling(window=10, min_periods=0).mean())
            #analysis.loc[i] =  [ticker  ,  df['10ma'].iloc[320]/df['10ma'].iloc[1] ]
            #analysis[ticker]  = [  df['10ma'].iloc[320]/df['10ma'].iloc[1] ]
            if df.shape[0]==321:
                analysis.loc[ticker,'drop ratio']  = [  df.loc['2020-04-09','10ma']/df.loc['2020-01-06','10ma'] ]
                analysis.loc[ticker,'price on 04-09']  = [  df.loc['2020-04-09','Adj Close'] ]
            print(ticker,i)
            try:
                temp=pbratio4.get_price2book(ticker)    
                analysis.loc[ticker,'pb']  = [ temp[0] ]
                analysis.loc[ticker,'roe']  = [ temp[1] ]
                analysis.loc[ticker,'market cap']  = [ temp[2] ]
                analysis.loc[ticker,'Debt/Eq']  = [ temp[3] ]
                analysis.loc[ticker,'Dividend %']  = [ temp[4] ]
            except:
                print("An exception occurred")
        else:
            print('Already have {}'.format(ticker))


    analysis.to_csv("500_analysis.csv")

analyse_data_from_yahoo()



