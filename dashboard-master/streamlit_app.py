import time
import streamlit as st
import pandas as pd
import numpy as np
import plost
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import pickle
import functions
import hvplot
import hvplot.pandas
from io import BytesIO
import pyautogui


def rerun_script():

    pyautogui.hotkey("ctrl","F5")
    st.experimental_rerun()

st.set_option('deprecation.showPyplotGlobalUse', False)  #<-- This disables plot warnings in streamlit


if 'list_of_selected_sectors' not in st.session_state:

        list_of_selected_sectors = []
else:
        list_of_selected_sectors = st.session_state.list_of_selected_sectors

if 'sum' not in st.session_state:

        sum = 0
else:
        sum = st.session_state.sum


#if 'list_of_selected_sectors' in st.session_state:

#list_of_selected_sectors = []

# Page setting

st.set_page_config(layout="wide")

with open('style.css') as f:
    test = 'test'
    #st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Data  ###################################################


# Get yahoo finance data

   # <-- Add tickers here ['MSFT', 'GOOG', 'SPY', 'GLD', 'XLV'] 

tickers_and_data_df = pd.DataFrame({})


# Iterate through list of yahoo tickers and append to dataframe

#for ticker in list_of_tickers_for_yahoo_data_dump:
    
    #single_ticker_df = functions.get_df_from_yahoo_finance(ticker)
    #tickers_and_data_df = pd.concat([tickers_and_data_df, single_ticker_df])



stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')


# Get Data from EconDB

#import house price index (for single family homes across US)

house_price_df = pd.read_csv('https://www.econdb.com/api/series/HOUUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import fed rates on long term bonds (10 year)
long_term_fed_rates_df = pd.read_csv('https://www.econdb.com/api/series/Y10YDUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import consumer price index (inflation)
cpi_df = pd.read_csv('https://www.econdb.com/api/series/CPIUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import consumer confidence index
consumer_confidence_df = pd.read_csv('https://www.econdb.com/api/series/CONFUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import M2 supply (all money circulating and in bank accounts)
money_supply_df = pd.read_csv('https://www.econdb.com/api/series/M3US/?format=csv', index_col='Date', parse_dates=['Date'])

#add columns to imitate yahoo df

cpi_df['Ticker'] = 'CPI'
cpi_df['Open'] = cpi_df['CPIUS']
cpi_df['High'] =cpi_df['CPIUS']
cpi_df['Low'] = cpi_df['CPIUS']
cpi_df['Close'] =cpi_df['CPIUS']
cpi_df['Adj Close'] = cpi_df['CPIUS']
cpi_df['Volume'] =cpi_df['CPIUS']
cpi_df = cpi_df.reset_index()
cpi_df = cpi_df.drop(['CPIUS'], axis=1)
cpi_df['Date'] = cpi_df['Date'].dt.strftime('%Y-%m-%d')

consumer_confidence_df['Ticker'] = 'CC'
consumer_confidence_df['Open'] = consumer_confidence_df['CONFUS']
consumer_confidence_df['High'] =consumer_confidence_df['CONFUS']
consumer_confidence_df['Low'] = consumer_confidence_df['CONFUS']
consumer_confidence_df['Close'] =consumer_confidence_df['CONFUS']
consumer_confidence_df['Adj Close'] = consumer_confidence_df['CONFUS']
consumer_confidence_df['Volume'] =consumer_confidence_df['CONFUS']
consumer_confidence_df = consumer_confidence_df.reset_index()
consumer_confidence_df = consumer_confidence_df.drop(['CONFUS'], axis=1)
consumer_confidence_df['Date'] = consumer_confidence_df['Date'].dt.strftime('%Y-%m-%d')

long_term_fed_rates_df['Ticker'] = 'Fed_Rates'
long_term_fed_rates_df['Open'] = long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['High'] =long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Low'] = long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Close'] =long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Adj Close'] = long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Volume'] =long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df = long_term_fed_rates_df.reset_index()
long_term_fed_rates_df = long_term_fed_rates_df.drop(['Y10YDUS'], axis=1)
long_term_fed_rates_df['Date'] = long_term_fed_rates_df['Date'].dt.strftime('%Y-%m-%d')

money_supply_df['Ticker'] = 'M3'
money_supply_df['Open'] = money_supply_df['M3US']
money_supply_df['High'] =money_supply_df['M3US']
money_supply_df['Low'] = money_supply_df['M3US']
money_supply_df['Close'] =money_supply_df['M3US']
money_supply_df['Adj Close'] = money_supply_df['M3US']
money_supply_df['Volume'] =money_supply_df['M3US']
money_supply_df = money_supply_df.reset_index()
money_supply_df = money_supply_df.drop(['M3US'], axis=1)
money_supply_df['Date'] = money_supply_df['Date'].dt.strftime('%Y-%m-%d')


####################################################################
    
# Add sidebar

with st.sidebar:
    st.write(sum)
    st.sidebar.markdown("<center><h1 style= text-align: center; color: black;>Please Select Industries</center>", unsafe_allow_html=True)

    with st.form(key='sector_selector'):
            
            
            left, right = st.columns(2)
            option = [0] * 16

            with left: 

                option[0] = [st.checkbox('S&P 500 ETF'), 'SPY']
                option[1] = [st.checkbox('Gold ETF'), 'GLD']
                option[2] = [st.checkbox('Volatility Index'), '^VIX']
                option[3] = [st.checkbox('Nasdaq Index'), 'QQQ']
                option[4] = [st.checkbox('Long Term Fed Rates'), 'Fed_Rates']
                option[5] = [st.checkbox('Consumer Confidence'), 'CC']
                option[6] = [st.checkbox('Money Supply'), 'M3']
                option[7] = [st.checkbox('NFT Market Cap'), 'NFT-USD']

            with right:
                
                option[8] = [st.checkbox('Bitcoin'), 'BTC-USD']
                option[9] = [st.checkbox('Healthcare ETF'), 'VHT']
                option[10] = [st.checkbox('Energy ETF'), 'XLE']
                option[11] = [st.checkbox('Industrials ETF'), 'XLI']
                option[12] = [st.checkbox('Consumer Price Index'), 'CPI']
                option[13] = [st.checkbox('Financial Sector ETF'), 'XLF']
                option[14] = [st.checkbox('Bond Index'), 'BND']
                option[15] = [st.checkbox('Multiverse Index'), 'MVS-USD']



            st.write('')

            
            end_date = datetime.date.today()
            start_date = datetime.date(1980, 1, 1)
            
            slider_range = st.slider("Select Date Range", value=[start_date, end_date])


            i = 0

            banned_ticker_list = ['CC','CPIUS', 'Fed_Rates', 'M3']
            
            for item in option:

                    sum = sum + option[i][0]

                    if (option[i][0] is True) and (option[1][1] != True):

                        option_ = option[i][1]
                        list_of_selected_sectors.append(option_)
                        
                    i = i + 1
                    

            
            for sector in list_of_selected_sectors:

                if sector not in banned_ticker_list:
            
                    single_ticker_df = functions.get_df_from_yahoo_finance(sector) #Make Yahoo data call based on selections
                    tickers_and_data_df = pd.concat([tickers_and_data_df, single_ticker_df])


            col1, col2, col3 = st.columns(3)

            with col1:
                pass
            with col3:
                pass
            with col2:
                submit_button = st.form_submit_button(label='Submit')
         

    col1, col2, col3 = st.columns(3)

    with col1:
        pass
    with col2:

        if sum != 0:
                
             if st.button('Monte Carlo'):
                 sum = -1
        else:

             pass
        
    with col3:
            
        pass

    st.session_state.sum = sum
    
    st.button('Reboot App',on_click=rerun_script)

#############################################################################

if sum == -1: #Run the monte carlo
        
    sum = -1
    st.markdown("<h1 style='text-align: center; color: black;'>Monte Carlo</h1>", unsafe_allow_html=True)
    #st.write(list_of_selected_sectors)
    st.write(f"the sum is {sum}")
    st.markdown("<h0 style='text-align: center; color: black; font-size: 15pt;'>To run the monte carlo please weight the.\
                  sectors in your portfolio.</h0>", unsafe_allow_html=True)
    
    def run_monte_carlo(sum):

        
        st.markdown("<h1 style='text-align: center; color: black;'>Monte Carlo</h1>", unsafe_allow_html=True)
        st.write(list_of_selected_sectors)
        st.write(f"the sum is {sum}")
        st.markdown("<h0 style='text-align: center; color: black; font-size: 15pt;'>To run the monte carlo please weight the.\
                  sectors in your portfolio.</h0>", unsafe_allow_html=True)
        sum = -1 - len(list_of_selected_sectors)
        st.session_state.sum = sum

    
    st.button('Messi',on_click=run_monte_carlo(sum))


############################################################################
    

if sum != 0: #Get data if any boxes are checked
        
    #st.write(list_of_selected_sectors)
    
    if 'CC' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, consumer_confidence_df], axis=0)

    if 'CPI' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, cpi_df], axis=0)
        
    if 'M3' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, money_supply_df], axis=0)

    if 'Fed_Rates' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, long_term_fed_rates_df], axis=0)

    

    tickers_and_data_df['Change'] = tickers_and_data_df['Close'] - tickers_and_data_df['Close'].shift(-1)
    tickers_and_data_df['Pct_Change'] = 100 * (tickers_and_data_df['Change'] / tickers_and_data_df['Close'].shift(-1))
    tickers_and_data_df['Date'] = pd.to_datetime(tickers_and_data_df['Date'], infer_datetime_format=True)
    tickers_and_data_df = tickers_and_data_df.drop_duplicates(subset=['Ticker', 'Date'], keep='last')

    pivoted_tickers_and_data_df_ = tickers_and_data_df.pivot(index="Date", columns="Ticker")
    pivoted_tickers_and_data_df = pivoted_tickers_and_data_df_.dropna()


if sum == 0: #Welcome page - nothing checked

    st.markdown("<h1 style='text-align: center; color: black;'>Welcome To The Zoom Team 6 Correlation Analyzer</h1>", unsafe_allow_html=True)
    st.write()
    st.write('')
    st.markdown("<h0 style='text-align: center; color: black; font-size: 15pt;'>This application conducts correlation studies between economic sectors and various indices. \
                  Please select the indices you would like to study from the sidebar on the left.\
                  </h0>", unsafe_allow_html=True)

if sum == 2:


    st.markdown(f"<center><h0 style='text-align: center; color: black; font-size: 30pt;'>Comparison of {list_of_selected_sectors[0]} and {list_of_selected_sectors[1]}</center></h0>",unsafe_allow_html=True )

    # Row A

    a1, a2 = st.columns(2)

    with a1: #2 tickers selected  -- This is histogram of correlated periods

        #Render histogram for 2 ticker correlation analysis
        histogram_data_ = pivoted_tickers_and_data_df['Pct_Change']
        histogram_data_['Correlation']  = histogram_data_[list_of_selected_sectors[0]].rolling(3).corr(histogram_data_[list_of_selected_sectors[1]])
        fig = plt.figure() 
        sns.histplot(data=histogram_data_, x='Correlation').set(title='Counts Of Correlated Periods')
        
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.
        

        
    with a2:  #2 tickers selected  -- This is bar plot of all periods by correlation

        #Render bar plot for 2 ticker correlation analysis
        fig = plt.figure() 
        bar_plot = sns.barplot(x=histogram_data_.index, y="Correlation",  data=histogram_data_)
        bar_plot.set(title='Correlated Periods Bar Chart')

        
        for index, label in enumerate(bar_plot.get_xticklabels()):    #Declutter the x-axis labels
                
            if index % 70 == 0:
                label.set_visible(True)
            else:
                label.set_visible(False)

               
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.
        

    # Row B
    
    b1 = st.columns(1)

    line_plot_data = {}
    pivoted_plot_data_df = {}
    line_plot_data = tickers_and_data_df[tickers_and_data_df['Ticker'].isin(list_of_selected_sectors)]

    if 'SPY' in list_of_selected_sectors:

        pass

    else:
        spy_data = functions.get_df_from_yahoo_finance('SPY')
        spy_data['Change'] = spy_data['Close'] - spy_data['Close'].shift(-1)
        spy_data['Pct_Change'] = 100 * (spy_data['Change'] / spy_data['Close'].shift(-1))
        line_plot_data = pd.concat([line_plot_data, spy_data], axis=0)
        
    line_plot_data['Date'] = pd.to_datetime(line_plot_data['Date'], infer_datetime_format=True)

                             
    pivoted_plot_data_df = line_plot_data.pivot(index="Date", columns="Ticker")
    pivoted_plot_data_df = pivoted_plot_data_df.dropna()
    
    pct_change = pivoted_plot_data_df['Pct_Change']
    pivoted_plot_data_df = pivoted_plot_data_df['Close']
    rolling_var_spy = pct_change['SPY'].rolling(window=3).var()

    rolling_beta = functions.rolling_beta_calculate(list_of_selected_sectors, pct_change, rolling_var_spy)
    rolling_beta.index=pd.to_datetime(rolling_beta.index, infer_datetime_format=True)
    rolling_beta = rolling_beta.iloc[::2, :]
    rolling_beta = rolling_beta.iloc[::2, :]

 
    rolling_beta = rolling_beta.reset_index()

    rolling_beta = rolling_beta.dropna()

    
    
    fig = plt.figure()

    i=0
    bar_plot = []

    color = ['black','red','green','orange','blue','limegreen','darkgreen','royalblue','navy']
    sns.set()
    
    for sector in list_of_selected_sectors:
    
        bar_plot.append(sns.barplot(data=rolling_beta, x='Date', y=sector, color=color[i]))
        i = i + 1


    st.write(fig)


   


        
    # Row C
    
    c1 = st.columns(1)

    line_plot_data = tickers_and_data_df[tickers_and_data_df['Ticker'].isin(list_of_selected_sectors)]
    pivoted_plot_data_df = line_plot_data.pivot(index="Date", columns="Ticker")
    pivoted_plot_data_df = pivoted_plot_data_df.dropna()
    
    fig = plt.figure() 
        
            
    line_plot = pivoted_plot_data_df.hvplot.line(x='Date', y= list_of_selected_sectors)
    line_plot.opts(legend_position='top_left')
    st.write(hvplot.render(line_plot))
    

if sum > 2:

    
    st.markdown(f"<center><h0 style='text-align: center; color: black; font-size: 30pt;'>Multi Sector Comparison</center></h0>",unsafe_allow_html=True )
    

      
    # Row A

    a1, a2= st.columns(2)

    with a1:

        
        fig = plt.figure()
        correlation_heatmap = sns.heatmap(pivoted_tickers_and_data_df['Pct_Change'].corr(), annot = True, cmap="YlGnBu")
                                          
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.
        
    with a2:

        plot_data = pivoted_tickers_and_data_df['Pct_Change']
        plot_data = plot_data.unstack(level=-1)
        plot_data = plot_data.reset_index()
        plot_data.columns = ['Ticker', 'Date', 'Value']
        
        
        fig = plt.figure() 
        box_plot = sns.boxplot(x= plot_data['Ticker'], y=plot_data['Value'], palette="Blues")

        
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.


    # Row B

 
    b1 = st.columns(1)

    line_plot_data = {}
    pivoted_plot_data_df = {}
    line_plot_data = tickers_and_data_df[tickers_and_data_df['Ticker'].isin(list_of_selected_sectors)]

    if 'SPY' in list_of_selected_sectors: #If spy is selected in sidebar, no need to import spy_data

        pass

    else:
        spy_data = functions.get_df_from_yahoo_finance('SPY')
        spy_data['Change'] = spy_data['Close'] - spy_data['Close'].shift(-1)
        spy_data['Pct_Change'] = 100 * (spy_data['Change'] / spy_data['Close'].shift(-1))
        line_plot_data = pd.concat([line_plot_data, spy_data], axis=0)
        
    line_plot_data['Date'] = pd.to_datetime(line_plot_data['Date'], infer_datetime_format=True)

                             
    pivoted_plot_data_df = line_plot_data.pivot(index="Date", columns="Ticker")
    pivoted_plot_data_df = pivoted_plot_data_df.dropna()
    
    pct_change = pivoted_plot_data_df['Pct_Change']
    pivoted_plot_data_df = pivoted_plot_data_df['Close']
    rolling_var_spy = pct_change['SPY'].rolling(window=3).var()

    rolling_beta = functions.rolling_beta_calculate(list_of_selected_sectors, pct_change, rolling_var_spy)
    rolling_beta.index=pd.to_datetime(rolling_beta.index, infer_datetime_format=True)
    rolling_beta = rolling_beta.iloc[::2, :]
    rolling_beta = rolling_beta.iloc[::2, :]

 
    rolling_beta = rolling_beta.reset_index()

    rolling_beta = rolling_beta.dropna()

    
    
    fig = plt.figure()

    i=0
    bar_plot = []

    color = ['navy','turquoise','blue','limegreen','darkgreen','royalblue','green', 'black']
    sns.set()
    
    for sector in list_of_selected_sectors:
    
        bar_plot.append(sns.barplot(data=rolling_beta, x='Date', y=sector, color=color[i]))
        i = i + 1
    sns.set_context(rc = {'patch.linewidth': 0.0})

    st.write(fig)







    # Row C
    
    c1 = st.columns(1)

    
    line_plot_data = tickers_and_data_df[tickers_and_data_df['Ticker'].isin(list_of_selected_sectors)]
    pivoted_plot_data_df = line_plot_data.pivot(index="Date", columns="Ticker")
    pivoted_plot_data_df = pivoted_plot_data_df.dropna()
    pivoted_plot_data_df = pivoted_plot_data_df['Close']

      
    fig = plt.figure() 
        
            
    line_plot = pivoted_plot_data_df.hvplot.line(x='Date', y= list_of_selected_sectors)
    line_plot.opts(legend_position='top_left')
    st.write(hvplot.render(line_plot))
    
    
