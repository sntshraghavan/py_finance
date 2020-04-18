import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader


style.use('ggplot')

start = dt.datetime(2010, 1, 1)
end = dt.datetime(2015, 1, 1)
#start = dt.datetime(2015, 1, 1)
#end = dt.datetime.now()
print(pandas_datareader.__version__)
df = web.DataReader("MMM", 'yahoo', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
#df = df.drop("Symbol", axis=1)

print(df.head())
