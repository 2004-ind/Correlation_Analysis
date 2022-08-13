def get_df_from_yahoo_finance (symbol): 

    import pandas as pd
    import datetime
    import urllib.request
    
    end_date = datetime.datetime.now()
    end_date = int(round(end_date.timestamp())) * 1000  #<-- Convert datetime to milliseconds 
    end_date_str = str(end_date)
    end_date_str = end_date_str[:10]  #<-- This removes all but the last 10 millisecond values for the time which is format yahoo wants

    start_date_str = '345427200'
  

    ticker_dataframe = {}
    

    # Build Yahoo finance URL for the data request.
    
    yahoo_finance_url_with_symbol = ('https://query1.finance.yahoo.com/v7/finance/download/' + str(symbol)
                                     + '?period1=' + str(start_date_str) + '&period2=' + str(end_date_str)
                                     + '&interval=1mo&events=history&includeAdjustedClose=true')

    url2 = urllib.request.urlopen(yahoo_finance_url_with_symbol) #request data (comes as CSV)
    
    ticker_dataframe = pd.read_csv(url2)  #convert CSV in memory from the Yahoo request to dataframe
    ticker_dataframe.insert(1, "Ticker", symbol)

    return (ticker_dataframe)

def get_df_from_yahoo_finance_by_day (symbol): 

    import pandas as pd
    import datetime
    import urllib.request
    
    end_date = datetime.datetime.now()
    end_date = int(round(end_date.timestamp())) * 1000  #<-- Convert datetime to milliseconds 
    end_date_str = str(end_date)
    end_date_str = end_date_str[:10]  #<-- This removes all but the last 10 millisecond values for the time which is format yahoo wants

    start_date_str = '345427200'
  

    ticker_dataframe = {}
    

    # Build Yahoo finance URL for the data request.
    
    yahoo_finance_url_with_symbol = ('https://query1.finance.yahoo.com/v7/finance/download/' + str(symbol)
                                     + '?period1=' + str(start_date_str) + '&period2=' + str(end_date_str)
                                     + '&interval=1d&events=history&includeAdjustedClose=true')

    url2 = urllib.request.urlopen(yahoo_finance_url_with_symbol) #request data (comes as CSV)
    
    ticker_dataframe = pd.read_csv(url2)  #convert CSV in memory from the Yahoo request to dataframe
    ticker_dataframe.insert(1, "Ticker", symbol)

    return (ticker_dataframe)


def rolling_beta_calculate(list, pct_change,  rolling_var_spy):

    import pandas as pd
    rolling_cov =pd.DataFrame()
    rolling_beta=pd.DataFrame()
    
    for ticker in list:
        rolling_cov[ticker]=pct_change[ticker].rolling(window=3).cov(pct_change['SPY'])
        rolling_beta[ticker] = rolling_cov[ticker]/rolling_var_spy
        print(f"{ticker}")
    return rolling_beta
    
    
    
def sharpe_ratio_calculator(list,pct_change):
    import numpy as np
    import pandas as pd
    sharpe_dict = {}
    std = pct_change.std()
    rows_list =[]
    for ticker in list:
        annualized_std = std[ticker]*np.sqrt(12)
        average_annual_return = pct_change[ticker].mean()*12
        sharpe_ratio = average_annual_return/annualized_std
        #print(f"{ticker} sharpe ratio = {sharpe_ratio}")
        sharpe_dict.update({ticker:sharpe_ratio})
        rows_list.append(sharpe_dict)
    sd = pd.DataFrame(rows_list)
    return sd

def sharpe_ratio_calculator_original(list,pct_change):
    import numpy as np
    import pandas as pd
    sharpe_dict = {}
    std = pct_change.std()
    rows_list =[]
    for ticker in list:
        annualized_std = std[ticker]*np.sqrt(12)
        average_annual_return = pct_change[ticker].mean()*12
        sharpe_ratio = average_annual_return/annualized_std
        #print(f"{ticker} sharpe ratio = {sharpe_ratio}")
        sharpe_dict.update({ticker:sharpe_ratio})
    return sharpe_dict


def mckenzie_test(list_of_tickers, new_potential_holding, sharpe_dict, corr_df):
    sharpe_sum = 0
    corr_sum = 0
    for ticker in list_of_tickers:
        if ticker in sharpe_dict:
            sharpe_sum = sharpe_dict[ticker] + sharpe_sum
    for ticker in list_of_tickers:
        corr_sum += corr_df.loc[ticker,new_potential_holding]
    corr_average =corr_sum/len(list_of_tickers)
    sharpe_ratio_average_of_portfolio = sharpe_sum/len(list_of_tickers)
    if sharpe_dict[new_potential_holding] > (sharpe_ratio_average_of_portfolio * corr_average):
        #print (f"{new_potential_holding} passes the McKenzie test and should be evaluated futher for your portfolio.")
        #print(f"The sharpe ratio of your current holding {current_holding} is {sharpe_dict[current_holding]} and {sharpe_dict[new_potential_holding]} for your new potential holding")
        #print(f"The expected correlation is {corr_df.loc[current_holding,new_potential_holding]}")
        #print(f"So therefore {corr_df.loc[current_holding,new_potential_holding]} * {sharpe_dict[current_holding]} is < {sharpe_dict[new_potential_holding]} so you should this passes the test")
        #return print (f"{new_potential_holding} passes the McKenzie test and should be evaluated futher for your portfolio.")
        return f"yes {new_potential_holding} passes the McKenzie test"
    else:
        #print(f"{new_potential_holding} does not pass the McKenzie test")
        #return print (f"{new_potential_holding} passes the McKenzie test and should be evaluated futher for your portfolio.")
        return f"no {new_potential_holding} does not pass the McKenzie test"
