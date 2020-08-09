import os
import datetime as dt
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
        symbols = ['$SPX'] + symbols


    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close', 'Volume'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df_temp = df_temp.rename(columns={'Volume': "Volume of " +symbol})
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
    dfmy=df.copy()
    dfmy['Daily_Delta']=0
    dfmy['Symbol']='IBM'
    dfmy['Order']='None'
    dfmy['rolling_mean_20']= pd.rolling_mean(df['IBM'], window=20)
    dfmy['direction of rolling mean']=0
    dfmy['Market Indicator']=0
    dfmy['rolling_std'] = pd.rolling_std(df['IBM'], window=20)
    dfmy['upper_band'] = dfmy['rolling_mean_20'] + 2.0*dfmy['rolling_std']
    dfmy['lower_band'] = dfmy['rolling_mean_20'] - 2.0*dfmy['rolling_std']
    dfmy['Bull_Market']=0
    dfmy['Bear_Market']=0
    dfmy['long execute']=0
    dfmy['long enter price']=0
    dfmy['long exit']=0
    dfmy['short execute']=0
    dfmy['short enter price']=0
    dfmy['short exit']=0
    dfmy['shares']=0
    dfmy['Shares']=0
    dfmy['Cash']=0
    dfmy['Cash'].ix[start_date]= start_val
    dfmy['Trades']=0
    dfmy['Cummulative_Value']=0
    dfmy1=dfmy.copy()
    dfmy1=dfmy1[np.isfinite(dfmy1['upper_band'])]
    dfmy1['Cash'].ix[start_date]= start_val

    buys = list()

    for i, row in dfmy1.iterrows():

        j= dfmy1.index.get_loc(i)
        if j > 1:
            dfmy1.ix[i,'Daily_Delta']=100*((dfmy1.ix[i, 'IBM'] - dfmy1.iloc[(dfmy1.index.get_loc(i) - 1)]['IBM'])/dfmy1.iloc[(dfmy1.index.get_loc(i) - 1)]['IBM'])

            if (dfmy1.ix[i, 'rolling_mean_20'] >= dfmy1.iloc[(dfmy1.index.get_loc(i) - 1)]['rolling_mean_20']):

                dfmy1.ix[i,'direction of rolling mean']=1


            if (dfmy1.ix[i, 'rolling_mean_20'] < dfmy1.iloc[(dfmy1.index.get_loc(i) - 1)]['rolling_mean_20']):

                dfmy1.ix[i,'direction of rolling mean']=0
            #Determiniting the direction of the Market

            dfmy1['Market Indicator']= pd.rolling_mean(dfmy1['direction of rolling mean'], window=5)
            if (dfmy1.ix[i, 'Market Indicator']>= 0.8):
                dfmy1.ix[i, 'Bull_Market'] =70
            else:
                dfmy1.ix[i, 'Bull_Market'] =0

            if (dfmy1.ix[i, 'Market Indicator']<= 0.2):
                dfmy1.ix[i, 'Bear_Market'] =70
            else:
                dfmy1.ix[i, 'Bear_Market'] =0

            #Conditions for taking a position
            if (dfmy1.ix[i, 'shares']==0):
                #Execute Long
                if (dfmy1.ix[i, 'IBM'] < dfmy1.ix[i, 'rolling_mean_20']) and (dfmy1.ix[i, 'Market Indicator']>=0.8):

                    dfmy1.ix[i:, 'shares']=100
                    dfmy1.ix[i, 'long execute']= 1
                    dfmy1.ix[i, 'Trades']= 100*(dfmy1.ix[i, 'IBM'])
                    dfmy1.ix[i, 'Order']= 'BUY'
                    dfmy1.ix[i:, 'Shares']=100
                    dfmy1.ix[i:, 'long enter price']= (dfmy1.ix[i, 'IBM'])
                    continue
                #Execute Short
                if (dfmy1.ix[i, 'IBM'] > dfmy1.ix[i, 'rolling_mean_20']) and (dfmy1.ix[i, 'Market Indicator']<=0.2):

                    dfmy1.ix[i:, 'shares']=-100
                    dfmy1.ix[i, 'short execute']= 1
                    dfmy1.ix[i, 'Trades']= -100*(dfmy1.ix[i, 'IBM'])
                    dfmy1.ix[i, 'Order']= 'SELL'
                    dfmy1.ix[i:, 'Shares']=100
                    dfmy1.ix[i:, 'short enter price']= (dfmy1.ix[i, 'IBM'])
                    continue

            #Condition to exit any position

            #Exit Long
            if (dfmy1.ix[i, 'shares']==100):

                if ((dfmy1.ix[i, 'IBM'] > dfmy1.ix[i, 'upper_band']) or (dfmy1.ix[i, 'IBM'] < 0.985*(dfmy1.ix[i, 'long enter price']) or (dfmy1.ix[i, 'Market Indicator'])<=0.2)):
                    dfmy1.ix[i:, 'shares']=0
                    dfmy1.ix[i, 'long exit']= 1
                    dfmy1.ix[i, 'Trades']= -100*(dfmy1.ix[i, 'IBM'])
                    dfmy1.ix[i, 'Order']= 'SELL'
                    dfmy1.ix[i:, 'Shares']=100
                    dfmy1.ix[i:, 'long enter price']=0
                    continue

            #Exit Short
            if (dfmy1.ix[i, 'shares']==-100):
                if (dfmy1.ix[i,'Daily_Delta'] <= -5.6):
                    continue
                if (dfmy1.ix[i,'Daily_Delta'] <= -4.6 and dfmy1.iloc[(dfmy1.index.get_loc(i) - 1)]['Daily_Delta'] <= -5.6):
                    continue

                if ((dfmy1.ix[i, 'IBM'] < dfmy1.ix[i, 'lower_band']) or (dfmy1.ix[i, 'IBM'] > 1.01*(dfmy1.ix[i, 'short enter price']) or (dfmy1.ix[i, 'Market Indicator'])>=0.6)):
                    dfmy1.ix[i:, 'shares']=0
                    dfmy1.ix[i, 'short exit']=1
                    dfmy1.ix[i, 'Trades']= 100*(dfmy1.ix[i, 'IBM'])
                    dfmy1.ix[i, 'Order']= 'BUY'
                    dfmy1.ix[i:, 'Shares']=100
                    continue



    dfmy1['Cash'] =  start_val - dfmy1['Trades'].cumsum()
    dfmy1['Cummulative_Value'] = dfmy1['Cash'] + dfmy1['shares']*dfmy1['IBM']
    dfmy1.to_csv('check_MY_Strategey_3.csv')
    Short = dfmy1.loc[dfmy1['short execute'] ==1].index
    ShortExit = dfmy1.loc[dfmy1['short exit'] ==1].index
    Long = dfmy1.loc[dfmy1['long execute'] ==1].index
    LongExit = dfmy1.loc[dfmy1['long exit'] ==1].index

    #Plot raw SPY values, rolling mean and Bollinger Bands
    ax = dfmy1['IBM'].plot(title="The Donaher Strategy", label='IBM')
    dfmy1['rolling_mean_20'].plot(label='Rolling mean_20', ax=ax)
    dfmy1['upper_band'].plot(label='upper band', ax=ax)
    dfmy1['lower_band'].plot(label='lower band', ax=ax)
    dfmy1['Bull_Market'].plot(label='Rising Interval', ax=ax)
    dfmy1['Bear_Market'].plot(label='Falling Interval', ax=ax)
    pmin, pmax = ax.get_ylim()
    ax.vlines(x=Short, ymin=pmin, ymax=pmax, color ='r')
    ax.vlines(x=ShortExit, ymin=pmin, ymax=pmax, color ='k')
    ax.vlines(x=Long, ymin=pmin, ymax=pmax, color ='g')
    ax.vlines(x=LongExit, ymin=pmin, ymax=pmax, color ='k')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='lower right')
    plt.show()

    dfShorts= dfmy1.loc[dfmy1['short execute']==1]
    dfShortsExit= dfmy1.loc[dfmy1['short exit']==1]
    dfLong= dfmy1.loc[dfmy1['long execute']==1]
    dfLongExit= dfmy1.loc[dfmy1['long exit']==1]

    dforderstmp = pd.concat([dfShorts, dfShortsExit,dfLong, dfLongExit])
    dforders= dforderstmp[['Symbol','Order','Shares']].sort_index()
    dforders.to_csv('orders.csv', index_label='Date')


    print
    portvals = compute_portvals(orders_file = 'orders.csv', start_val = 10000)
    portvals.to_csv('check_MY_Strategey_3_BT.csv')

    start_date1 = ((portvals.index.min()).to_datetime()).strftime('%Y-%m-%d')
    end_date1 = ((portvals.index.max()).to_datetime()).strftime('%Y-%m-%d')
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
    print "Cummulative Return of $SPX: {} ".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Back Test Value: {}".format(portvals.ix[-1,['Cummulative_Value']][0])
    print "Final Portfolio Value on 12/31/2009: {}".format(dfmy1.ix[-1,['Cummulative_Value']][0])































if __name__ == "__main__":
    test_run()