import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import requests

def remove(string): 
    return string.replace(" ", "") 

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
        tickers.append(ticker.rstrip().upper())
    tickers.append("spy".upper())
    tick_df = pd.DataFrame(tickers) 
    tick_df.to_csv('sp500tickers.csv', index=False)
    return "done"


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
        #print(tickers)
        #tickers = save_dow_tickers()
        #print(tickers)
	
    else:
        ticker_csv = pd.read_csv('sp500tickers.csv', parse_dates=True, header=None)
        #ticker_csv = pd.read_csv('Airline.csv',      parse_dates=True, header=None)
 
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2019, 1, 1)
    end = dt.date.today() #datetime(2020, 4, 18)
    print(ticker_csv)
    for ticker in ticker_csv.iloc[:,0]:
        ticker=remove(ticker)
        # just in case your connection breaks, we'd like to save our progress!
        try:
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                print(ticker+" downloading") 
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.reset_index(inplace=True)
                df.set_index("Date", inplace=True)
                #df = df.drop("Symbol", axis=1)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
                df.set_index("Date", inplace=True)
                print('Already have {}'.format(ticker))
                print(df.tail(1).index.values[0])
                #print(df.tail(1)["Date"].to_string())
                #print(df.tail(1)["Date"].to_string(index=False))
                print(df.tail(1).index.values[0])
                date_last = dt.datetime.strptime(  df.tail(1).index.values[0] , '%Y-%m-%d')
                #print(df)
                #df.index.astype()
                #print(df.iloc[:,0])
                #print(df.index)
                if(end >date_last.date()):
                    df_new = web.DataReader(ticker, 'yahoo', (date_last+ dt.timedelta(days=1)).date() , end)#+ dt.timedelta(days=1)
                    df_new.iloc[:, 0]=df_new.iloc[:, 0].astype(str)
                    df_new.iloc[:, 0]=df_new.iloc[:, 0].astype(str)
                    #print(df_new.index)
                    df_new.index=df_new.index.strftime('%Y-%m-%d')
                    #df_new['Date']=df_new['Date'].dt.date
                    #df_new.reset_index(inplace=True)
                    #df_new["Date"]=
                    #print(df_new["Date"])
                    #print(type(df_new.High))
                    #print(type(df_new.Date))
                    #df_new.set_index("Date", inplace=True)
                    #print(type(df.index))
                    #print(type(df_new.index))
                    df=df.append(df_new)
                    #print(df)
                    df.to_csv('stock_dfs/{}.csv'.format(ticker))
        except:
           print("failed to download {}".format(ticker))



#    analysis = pd.DataFrame(columns=['tick', 'ratio'],index=range(0,500) )
#            #df['10ma']=(df['Adj Close'].rolling(window=10, min_periods=0).mean())
#            #print(df.shape)
#            #print(df['10ma'].iloc[1])
#            print(df['10ma'].iloc[320]/df['10ma'].iloc[1])
#            analysis.loc[i] =  [ticker  ,  df['10ma'].iloc[320]/df['10ma'].iloc[1] ]
#            print(analysis)

#save_sp500_tickers()
get_data_from_yahoo()



