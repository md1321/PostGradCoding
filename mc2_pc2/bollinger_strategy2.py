import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="/home/ml4t/data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols


    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close', 'Volume'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df_temp = df_temp.rename(columns={'Volume': "Volume of" +symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])
    print df
    return df

def test_run():
    start_val = 10000
    # Read data
    dates = pd.date_range('2009-12-31', '2011-12-31')
    symbols = ['IBM']
    df = get_data(symbols, dates)
    dfBol=df.copy()
    start_date = dfBol.index.min()
    dfBol['Symbol']='IBM'
    dfBol['Order']='None'
    dfBol['rolling_mean']= pd.rolling_mean(df['IBM'], window=20)
    dfBol['rolling_std'] = pd.rolling_std(df['IBM'], window=20)
    dfBol['upper_band'] = dfBol['rolling_mean'] + 2*dfBol['rolling_std']
    dfBol['lower_band'] = dfBol['rolling_mean'] - 2*dfBol['rolling_std']
    dfBol['long execute']=0
    dfBol['long exit']=0
    dfBol['short execute']=0
    dfBol['short exit']=0
    dfBol['shares']=0
    dfBol['Shares']=0
    dfBol['Cash']=0
    dfBol['Cash'].ix[start_date]= start_val
    dfBol['Trades']=0
    dfBol['Cummulative_Value']=0
    dfBol1=dfBol.copy()
    dfBol1=dfBol1[np.isfinite(dfBol1['upper_band'])]
    dfBol1['Cash'].ix[start_date]= start_val

    buys = list()

    for i, row in dfBol1.iterrows():

        j= dfBol1.index.get_loc(i)
        print j
        if j > 0:
            print i
            print "Shares of IBM", dfBol1.ix[i, 'shares']
            print "Stock Price day before", dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['IBM']
            print "Stock Price today", dfBol1.ix[i, 'IBM']
            print "lower band today",dfBol1.ix[i, 'lower_band']
            print "upper band day before", dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['upper_band']
            print "lower band day before", dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['lower_band']
            if (dfBol1.ix[i, 'shares']==0):
                if ((dfBol1.ix[i, 'IBM'] < dfBol1.ix[i, 'upper_band']) and (dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['IBM'] > dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['upper_band'])):
                    print "=============================="
                    print " Upper cross seen, short 100 shares on ", i
                    print "=============================="
                    dfBol1.ix[i:, 'shares']=-100
                    dfBol1.ix[i, 'short execute']= 1
                    dfBol1.ix[i, 'Trades']= -100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'SELL'
                    dfBol1.ix[i:, 'Shares']=100
    #       print dfBol1.ix[i, 'sell trigger loaded']
                if ((dfBol1.ix[i, 'IBM'] > dfBol1.ix[i, 'lower_band']) and (dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['IBM'] < dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['lower_band'])):
                    print "=============================="
                    print " Lower cross seen, buy 100 shares on ", i
                    print "=============================="
                    dfBol1.ix[i:, 'shares']=100
                    dfBol1.ix[i, 'long execute']= 1
                    dfBol1.ix[i, 'Trades']= 100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'BUY'
                    dfBol1.ix[i:, 'Shares']=100
                else:

                    continue
            else:
                print "shares not equal to 0, no futher evaluation done"

            if (dfBol1.ix[i, 'shares']==100):
                if (dfBol1.ix[i, 'IBM'] > dfBol1.ix[i, 'rolling_mean']):
                    dfBol1.ix[i:, 'shares']=0
                    dfBol1.ix[i, 'long exit']= 1
                    dfBol1.ix[i, 'Trades']= -100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'SELL'
                    dfBol1.ix[i:, 'Shares']=100
                    print "=============================="
                    print "Exit Long, 100 shares sold on", i
                    print "=============================="
                else:
                    print "Still Holding"
            if (dfBol1.ix[i, 'shares']==-100):
                if (dfBol1.ix[i, 'IBM'] < dfBol1.ix[i, 'rolling_mean']):
                    dfBol1.ix[i:, 'shares']=0
                    dfBol1.ix[i, 'short exit']=1
                    dfBol1.ix[i, 'Trades']= 100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'BUY'
                    dfBol1.ix[i:, 'Shares']=100
                    print "=============================="
                    print "Exit Short 100 shares bought on", i
                    print "=============================="
                else:
                    print "Still Holding"
        else:
            continue

    dfBol1['Cash'] =  start_val - dfBol1['Trades'].cumsum()
    dfBol1['Cummulative_Value'] = dfBol1['Cash'] + dfBol1['shares']*dfBol1['IBM']
    dfBol1.to_csv('check_IBM2.csv')
    Short = dfBol1.loc[dfBol1['short execute'] ==1].index
    ShortExit = dfBol1.loc[dfBol1['short exit'] ==1].index
    Long = dfBol1.loc[dfBol1['long execute'] ==1].index
    LongExit = dfBol1.loc[dfBol1['long exit'] ==1].index

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = dfBol1['IBM'].plot(title="Bollinger Bands", label='IBM')
    dfBol1['rolling_mean'].plot(label='Rolling mean', ax=ax)
    dfBol1['upper_band'].plot(label='upper band', ax=ax)
    dfBol1['lower_band'].plot(label='lower band', ax=ax)
    pmin, pmax = ax.get_ylim()
    ax.vlines(x=Short, ymin=pmin, ymax=pmax, color ='r')
    ax.vlines(x=ShortExit, ymin=pmin, ymax=pmax, color ='k')
    ax.vlines(x=Long, ymin=pmin, ymax=pmax, color ='g')
    ax.vlines(x=LongExit, ymin=pmin, ymax=pmax, color ='k')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='lower right')
    plt.show()
    print "These are the Shorts", Short
    dfShorts= dfBol1.loc[dfBol1['short execute']==1]
    dfShortsExit= dfBol1.loc[dfBol1['short exit']==1]
    dfLong= dfBol1.loc[dfBol1['long execute']==1]
    dfLongExit= dfBol1.loc[dfBol1['long exit']==1]
    print dfShorts[['Symbol','Order','Shares']]
    print dfShortsExit[['Symbol','Order','Shares']]
    print dfLong[['Symbol','Order','Shares']]
    print dfLongExit[['Symbol','Order','Shares']]
    dforderstmp = pd.concat([dfShorts, dfShortsExit,dfLong, dfLongExit])
    dforders= dforderstmp[['Symbol','Order','Shares']].sort_index()
    print dforders
    dforders.to_csv('orders.csv', index_label='Date')

    print "These are the Short exits", ShortExit
    print "These are the Longs", Long
    print "These are the Long exits", LongExit
    print "The Cumulative return is:", dfBol1.ix[-1, ['Cummulative_Value']]



    # Add axis labels and legend



if __name__ == "__main__":
    test_run()