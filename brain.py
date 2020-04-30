import bs4 as bs
import datetime as dt
import os
import math
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import pbratio4 
import matplotlib.pyplot as plt 

def vis_data():
   df = pd.read_csv('500_analysis.csv')
   df2=df.sort_values(by=['drop_ratio']) 
   df2.to_csv("500_analysis_drop_ratio.csv")
   df['market_cap'].to_csv("500_analysis_mc.csv")

   for column in df:
    df[column] = pd.to_numeric(df[column],errors='coerce')
    fig, ax = plt.subplots()
    df[column].hist(bins=10).get_figure()
    plt.ylabel(column,fontsize=15)
    fig.savefig(column+'.pdf')
    try:
        print('average:',df[column].mean(axis=None, skipna=True)) 
        print('median:',df[column].median()) 
        print('std:',df[column].std(axis=None, skipna=True)) 
        print('min:',df[column].min()) 
        print('max:',df[column].max()) 
    except:
        print("error")

def find_data_cutoff(orig,percentage):
   ascend_=True
   df = pd.to_numeric(orig,errors='coerce')
   df=df.sort_values(ascending=ascend_)
   #df.to_csv(column+"count.csv")
   return(df.iloc[math.floor((500-df.isna().sum())*percentage)])

def filter_data(df,criteria):
    #for index, row in df.iterrows(): 
    for key, value in criteria.items():  
        if value[1]:
            df=df.loc[df[key] > value[0]]
        else:
            df=df.loc[df[key] < value[0]]
    print(df)
    df['values']=df['pb']*0+10
    df['date']=dt.date.today()
    df[['values','date']].to_csv("filtered.csv")





df = pd.read_csv('500_analysis.csv', index_col=[0])
for column in df:
    if column!="":
        df[column] = pd.to_numeric(df[column],errors='coerce')
name=df.columns 
criteria= {}
list_per=[.1,.2]
list_name=["drop_ratio","market_cap"]
list_ass=[False,True]  # False  < ;   True > 
#for arg in list_name:
i=0
while i < len(list_name):
    arg=list_name[i]
    criteria[arg]=[find_data_cutoff(df[arg],list_per[i]),list_ass[i]]
    i=i+1
print(criteria)
filter_data(df,criteria)
