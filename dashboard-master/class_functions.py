def get_df_from_yahoo_finance (symbol): 

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
