import os
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="/home/mdonaher/ml4t/data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols
        symbols = ['$SPX'] + symbols


    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close', 'Volume'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df_temp = df_temp.rename(columns={'Volume': "Volume of" +symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df

def compute_portvals(orders_file = "orders.csv", start_val = 1000):

    orderdf = pd.read_csv(orders_file,sep=',',index_col=[0])
    start_date = orderdf.index.min()  # getting start date of DF
    end_date = orderdf.index.max()   # getting end date of DF
    sortorderdf = orderdf.sort_index()

    symbols = pd.unique(sortorderdf.Symbol.ravel()).tolist()  # Getting unique list of symbols in a list

    portvals = get_data(symbols, pd.date_range(start_date, end_date)) # using utility to populate the DF with the stock proces per day
    portvals['Cash']=0  #Adding a column for the  cash value
    portvals['Cash'].ix[start_date]= start_val # setting the initial cash value to 1000000
    portvals['Trades']=0
    portvals['Leverage']=0
    portvals['Stock_Value'] = 0
    portvals['Cummulative_Value'] = 0

    for symbol in symbols:
        newcol = "Shares of "+symbol
        newcol2 ="Value of "+symbol
        newcol3 = "Transactions of "+symbol

        portvals[newcol]=0
        portvals[newcol2]=0
        portvals[newcol3]=0


    portvalstemp=portvals.copy()


    for i, row in sortorderdf.iterrows(): # iterating thru orders DF creating columns with Number of shares
        if i in portvalstemp.index:
            numShares = "Shares of "+row[0]
            sym = row[0]
            if row[1] == 'SELL':
                x = -1
            else:
                x=1
            shares = row[2] *x
            if (portvalstemp.ix[i, numShares] == 0):  # If then to account for if stocks are bought and sold on the same day
                portvalstemp.ix[i:, numShares] = shares# Enter value if there are already no transactions for that day
            else:
                portvalstemp.ix[i:, numShares] = shares + portvalstemp.ix[i, numShares]# Sum the latest transaction with the earlier one for that day

            newcol4 = "Transactions of "+row[0]
            newcol5 = "Value of "+row[0]

            if (portvalstemp.ix[i,newcol4] == 0):
                portvalstemp.ix[i,newcol4]= shares * portvalstemp.ix[i,row[0]]
            else:
                portvalstemp.ix[i,newcol4]= shares * portvalstemp.ix[i,row[0]] + portvalstemp.ix[i,newcol4]
            portvalstemp[newcol5]= portvalstemp[numShares] * portvalstemp[row[0]]
            portvalstemp['Trades'] = portvalstemp.filter(regex="Transactions of").sum(axis=1)
            portvalstemp['Cash'] =  start_val - portvalstemp['Trades'].cumsum()
            portvalstemp['Leverage'] = ((portvalstemp.filter(regex="Value of").abs()).sum(axis=1)/((portvalstemp.filter(regex="Value of").sum(axis=1)) +portvalstemp['Cash']))
            portvalstemp['Stock_Value'] = portvalstemp.filter(regex="Value of").sum(axis=1)
            portvalstemp['Cummulative_Value'] = ((portvalstemp.filter(regex="Value of").sum(axis=1)) + portvalstemp['Cash'])

            if (portvalstemp.loc[i]['Leverage'] <= 2.0 ):
                portvalsfinal = portvalstemp.copy()
            elif (portvalstemp.loc[i]['Leverage']< portvalstemp.iloc[(portvalstemp.index.get_loc(i) - 1)]['Leverage']):
                portvalsfinal = portvalstemp.copy()
            else:
                portvalstemp = portvalsfinal.copy()

            continue

    portvals =  pd.DataFrame(portvalsfinal[['$SPX','Cummulative_Value']])
    portvalsnorm = portvals/portvals.ix[0,:]
    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = portvalsnorm['Cummulative_Value'].plot(title="Daily Portfolio Value and $SPX", label='Portfolio')
    portvalsnorm['$SPX'].plot(label='$SPX', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price")
    ax.legend(loc='upper left')
    plt.show()

    return portvals





def test_run():
    start_val = 10000
    # Read data
    start_date = dt.datetime(2007,12,31)
    end_date =dt.datetime(2009,12,31)
    dates = pd.date_range(start_date, end_date)
    symbols = ['IBM']
    df = get_data(symbols, dates)
    dfBol=df.copy()
    dfBol['Symbol']='IBM'
    dfBol['Order']='None'
    #dfBol['rolling_mean']= pd.rolling_mean(df['IBM'], window=20)  #df['IBM']x.rolling(window=2).mean()
    dfBol['rolling_mean']= df['IBM'].rolling(window=20).mean()
    #dfBol['rolling_std'] = pd.rolling_std(df['IBM'], window=20)
    dfBol['rolling_std'] = df['IBM'].rolling(window=20).std()
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
    #dfBol1=dfBol1[np.isfinite(dfBol1['upper_band'])]
    dfBol1['Cash'].ix[start_date]= start_val

    for i, row in dfBol1.iterrows():

        j= dfBol1.index.get_loc(i)
        if j > 0:
            if (dfBol1.ix[i, 'shares']==0):
                if ((dfBol1.ix[i, 'IBM'] < dfBol1.ix[i, 'upper_band']) and (dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['IBM'] > dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['upper_band'])):
                    dfBol1.ix[i:, 'shares']=-100
                    dfBol1.ix[i, 'short execute']= 1
                    dfBol1.ix[i, 'Trades']= -100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'SELL'
                    dfBol1.ix[i:, 'Shares']=100
                    continue
    #       print dfBol1.ix[i, 'sell trigger loaded']
                if ((dfBol1.ix[i, 'IBM'] > dfBol1.ix[i, 'lower_band']) and (dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['IBM'] < dfBol1.iloc[(dfBol1.index.get_loc(i) - 1)]['lower_band'])):
                    dfBol1.ix[i:, 'shares']=100
                    dfBol1.ix[i, 'long execute']= 1
                    dfBol1.ix[i, 'Trades']= 100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'BUY'
                    dfBol1.ix[i:, 'Shares']=100
                    continue


            if (dfBol1.ix[i, 'shares']==100):
                if (dfBol1.ix[i, 'IBM'] > dfBol1.ix[i, 'rolling_mean']):
                    dfBol1.ix[i:, 'shares']=0
                    dfBol1.ix[i, 'long exit']= 1
                    dfBol1.ix[i, 'Trades']= -100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'SELL'
                    dfBol1.ix[i:, 'Shares']=100
                    continue

            if (dfBol1.ix[i, 'shares']==-100):
                if (dfBol1.ix[i, 'IBM'] < dfBol1.ix[i, 'rolling_mean']):
                    dfBol1.ix[i:, 'shares']=0
                    dfBol1.ix[i, 'short exit']=1
                    dfBol1.ix[i, 'Trades']= 100*(dfBol1.ix[i, 'IBM'])
                    dfBol1.ix[i, 'Order']= 'BUY'
                    dfBol1.ix[i:, 'Shares']=100
                    continue


    dfBol1['Cash'] =  start_val - dfBol1['Trades'].cumsum()
    dfBol1['Cummulative_Value'] = dfBol1['Cash'] + dfBol1['shares']*dfBol1['IBM']
    dfBol1.to_csv('check_IBM3.csv')
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

    dfShorts= dfBol1.loc[dfBol1['short execute']==1]
    dfShortsExit= dfBol1.loc[dfBol1['short exit']==1]
    dfLong= dfBol1.loc[dfBol1['long execute']==1]
    dfLongExit= dfBol1.loc[dfBol1['long exit']==1]

    dforderstmp = pd.concat([dfShorts, dfShortsExit,dfLong, dfLongExit])
    dforders= dforderstmp[['Symbol','Order','Shares']].sort_index()
    dforders.to_csv('orders.csv', index_label='Date')


    portvals = compute_portvals(orders_file = "orders.csv", start_val = 10000)

    dfBol1Cum = dfBol1['Cummulative_Value']
    dfBol1Cum.to_csv('Bolliger_Cummulative.csv')
    portvals.to_csv('My_Simulator.csv')

    start_date1 = ((portvals.index.min()).to_pydatetime()).strftime('%Y-%m-%d')
    end_date1 = ((portvals.index.max()).to_pydatetime()).strftime('%Y-%m-%d')
    calc_cum_ret = (portvals.ix[-1, ['Cummulative_Value']]/portvals.ix[0, ['Cummulative_Value']]) -1

    calc_adr = ((portvals['Cummulative_Value']/portvals['Cummulative_Value'].shift()) -1).mean()
    calc_sddr = ((portvals['Cummulative_Value']/portvals['Cummulative_Value'].shift()) -1).std()
    sharpe_ratio = (252)**0.5 * calc_adr/calc_sddr
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [calc_cum_ret[0],calc_adr,calc_sddr,sharpe_ratio]

    calc_cum_ret_SPX = (portvals.ix[-1, ['$SPX']]/portvals.ix[0, ['$SPX']]) -1
    calc_adr_SPX = ((portvals['$SPX']/portvals['$SPX'].shift()) -1).mean()
    calc_sddr_SPX = ((portvals['$SPX']/portvals['$SPX'].shift()) -1).std()
    sharpe_ratio_SPX = (252)**0.5 * calc_adr_SPX/calc_sddr_SPX
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = [calc_cum_ret_SPX[0],calc_adr_SPX,calc_sddr_SPX,sharpe_ratio_SPX]

    print "Date Range: {} to {}".format(start_date1, end_date1)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX : {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {} ".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Back Test Value: {}".format(portvals.ix[-1,['Cummulative_Value']][0])
    print "Final Portfolio Value on 12/31/2009: {}".format(dfBol1.ix[-1,['Cummulative_Value']][0])


    # Add axis labels and legend



if __name__ == "__main__":
    test_run()
