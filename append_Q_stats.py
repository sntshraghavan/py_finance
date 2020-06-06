import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import requests
import pbratio4 


def analyse_data_from_yahoo():
    ticker_csv = pd.read_csv('sp500tickers.csv', parse_dates=True, index_col=0)
    label_list=['drop_ratio','price_on_0409','pb','roe','market_cap','Debt_Eq','Dividend_','profit_margin','Corre_spy_last200','Corre_spy_last100']
    analysis = pd.DataFrame(columns=label_list)
    correlation = pd.DataFrame(columns=['spy', 'other'])
    spy = pd.read_csv('stock_dfs/{}.csv'.format('spy'), parse_dates=True, index_col=0)
    correlation['spy']=spy['Adj Close']
    #print(analysis)
    #print(correlation)
    #analysis = pd.DataFrame(columns=['tick', 'ratio'])
    i=0
    for ticker in ticker_csv.iloc[:,0]:
        i=i+1
        if os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), parse_dates=True, index_col=0)
            correlation['other']=df['Adj Close']
            print(ticker,df.shape,df.shape[0] )
            df['10ma']=(df['Adj Close'].rolling(window=10, min_periods=0).mean())
            #analysis.loc[i] =  [ticker  ,  df['10ma'].iloc[320]/df['10ma'].iloc[1] ]
            #analysis[ticker]  = [  df['10ma'].iloc[320]/df['10ma'].iloc[1] ]
            if df.shape[0]>328:
                analysis.loc[ticker,label_list[0]]  =   df.loc['2020-06-05','10ma']/df.loc['2020-02-14','10ma'] 
                analysis.loc[ticker,label_list[1]]  =   df.loc['2020-04-29','Adj Close'] 
                analysis.loc[ticker,label_list[8]]  = correlation.tail(200).corr().loc['spy','other'] 
                analysis.loc[ticker,label_list[9]]  = correlation.tail(100).corr().loc['spy','other'] 
            print(ticker,i)
            try:
                temp=pbratio4.get_price2book(ticker)    
                print(temp)
                analysis.loc[ticker,label_list[2]]  =  temp[0] 
                analysis.loc[ticker,label_list[3]]  =  temp[1] 
                analysis.loc[ticker,label_list[4]]  =  temp[2] 
                analysis.loc[ticker,label_list[5]]  =  temp[3] 
                analysis.loc[ticker,label_list[6]]  =  temp[4] 
                analysis.loc[ticker,label_list[7]]  =  temp[5] 
            except:
                print("An exception occurred")
        else:
            print('Already have {}'.format(ticker))

        #if i==2:
        #    break 
    analysis.to_csv("500_analysis.csv")

analyse_data_from_yahoo()



