import time
import streamlit as st
import pandas as pd
import numpy as np
import plost
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import functions
from io import BytesIO
import pyautogui
from MCForecastTools import MCSimulation
import urllib.request
import altair as alt

def rerun_script():

    pyautogui.hotkey("ctrl","F5")
    #st.experimental_rerun()

st.set_option('deprecation.showPyplotGlobalUse', False)  #<-- This disables plot warnings in streamlit


if 'list_of_selected_sectors' not in st.session_state: #<-- Determine status of session state variables and set {counter} apprpriately.

        list_of_selected_sectors = []
else:
        list_of_selected_sectors = st.session_state.list_of_selected_sectors

if 'counter' not in st.session_state:  #<-- the counter variable is used to maintain the session state between iterations.   

        counter = 0
        st.session_state.counter = counter
else:
        counter = st.session_state.counter
        
if 'counter2' not in st.session_state:

    st.session_state.counter2 = 0

else:
    if st.session_state.counter2 != 0:
        st.session_state.counter2 = -1
    

# Data  ###################################################


# Get yahoo finance data


tickers_and_data_df = pd.DataFrame({})
tickers_and_data_df_mc = pd.DataFrame({})
tickers_and_data_df_mc1 = pd.DataFrame({})

# Iterate through list of yahoo tickers and append to dataframe

# Get Monthly Data from EconDB 

#import house price index from EconDB (for single family homes across US)

house_price_df = pd.read_csv('https://www.econdb.com/api/series/HOUUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import fed rates on long term bonds (10 year)
long_term_fed_rates_df = pd.read_csv('https://www.econdb.com/api/series/Y10YDUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import consumer price index (inflation)
cpi_df = pd.read_csv('https://www.econdb.com/api/series/CPIUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import consumer confidence index
consumer_confidence_df = pd.read_csv('https://www.econdb.com/api/series/CONFUS/?format=csv', index_col='Date', parse_dates=['Date'])

#import M2 supply (all money circulating and in bank accounts)
money_supply_df = pd.read_csv('https://www.econdb.com/api/series/M3US/?format=csv', index_col='Date', parse_dates=['Date'])




#Reformat EconDB data to look like yahoo finance data.

cpi_df['Ticker'] = 'CPI'
cpi_df['Open'] = cpi_df['CPIUS']
cpi_df['High'] =cpi_df['CPIUS']
cpi_df['Low'] = cpi_df['CPIUS']
cpi_df['Close'] =cpi_df['CPIUS']
cpi_df['Adj Close'] = cpi_df['CPIUS']
cpi_df['Volume'] =cpi_df['CPIUS']
cpi_df = cpi_df.reset_index()
cpi_df = cpi_df.drop(['CPIUS'], axis=1)
cpi_df['Date'] = cpi_df['Date'].dt.date

consumer_confidence_df['Ticker'] = 'CC'
consumer_confidence_df['Open'] = consumer_confidence_df['CONFUS']
consumer_confidence_df['High'] =consumer_confidence_df['CONFUS']
consumer_confidence_df['Low'] = consumer_confidence_df['CONFUS']
consumer_confidence_df['Close'] =consumer_confidence_df['CONFUS']
consumer_confidence_df['Adj Close'] = consumer_confidence_df['CONFUS']
consumer_confidence_df['Volume'] =consumer_confidence_df['CONFUS']
consumer_confidence_df = consumer_confidence_df.reset_index()
consumer_confidence_df = consumer_confidence_df.drop(['CONFUS'], axis=1)
consumer_confidence_df['Date'] = consumer_confidence_df['Date'].dt.date

long_term_fed_rates_df['Ticker'] = 'Fed_Rates'
long_term_fed_rates_df['Open'] = long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['High'] =long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Low'] = long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Close'] =long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Adj Close'] = long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df['Volume'] =long_term_fed_rates_df['Y10YDUS']
long_term_fed_rates_df = long_term_fed_rates_df.reset_index()
long_term_fed_rates_df = long_term_fed_rates_df.drop(['Y10YDUS'], axis=1)
long_term_fed_rates_df['Date'] = long_term_fed_rates_df['Date'].dt.date

money_supply_df['Ticker'] = 'M3'
money_supply_df['Open'] = money_supply_df['M3US']
money_supply_df['High'] =money_supply_df['M3US']
money_supply_df['Low'] = money_supply_df['M3US']
money_supply_df['Close'] =money_supply_df['M3US']
money_supply_df['Adj Close'] = money_supply_df['M3US']
money_supply_df['Volume'] =money_supply_df['M3US']
money_supply_df = money_supply_df.reset_index()
money_supply_df = money_supply_df.drop(['M3US'], axis=1)
money_supply_df['Date'] = money_supply_df['Date'].dt.date



####################################################################
    
# Page setting

st.set_page_config(layout="wide")

# Add main navigation Sidebar

with st.sidebar:
    
    st.sidebar.markdown("<center><h1 style= text-align: center; color: black;>Please Select Industries</center>", unsafe_allow_html=True)
 
    with st.form(key='sector_selector'):
            
            left, right = st.columns(2)
            option = [0] * 16

            with left: 

                option[0] = [st.checkbox('S&P 500 ETF'), 'SPY']  #<-- These are the industry selector options.  [1] variable is yahoo ticker symbol.
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
                option[15] = [st.checkbox('Short Trm Treasury'), 'SHV']



            st.write('')

            
            end_date = datetime.date.today()
            start_date = datetime.date(2000, 1, 1)
            
            slider_range = st.slider("Select Date Range", value=[start_date, end_date])

            banned_ticker_list = ['CC', 'CPIUS', 'Fed_Rates', 'M3', 'CPI', 'CONFUS']    # <--Tickers to ignore in later functions

            i = 0
            for item in option:

                    counter = counter + option[i][0]

                    if (option[i][0] is True) and (option[1][1] != True):

                        option_ = option[i][1]
                        list_of_selected_sectors.append(option_)
                        
                    i = i + 1
                    

            
            for sector in list_of_selected_sectors:

                if sector not in banned_ticker_list:
            
                    single_ticker_df = functions.get_df_from_yahoo_finance(sector)              #<-- Make Yahoo data call based on selections
                    tickers_and_data_df = pd.concat([tickers_and_data_df, single_ticker_df])


            col1, col2, col3 = st.columns(3)  #<-- Only way to center objects in Streamlit.

            with col1:
                pass
            with col3:
                pass
            with col2:
                submit_button = st.form_submit_button(label='Submit')
         

    col1 = st.columns(1)

    
    weights = {}
    if counter != 0:
         with st.expander("Monte Carlo", expanded=False): #<-- Only display monte carlo expander in second iteration after tickers are selected.
             with st.form(key='monte_carlo'):
                 year_selectbox = st.selectbox('Select Number Of Years', ['<none>',5,10,15,20])
                 

                 i = 0
                 for sector in list_of_selected_sectors:
                     if sector not in banned_ticker_list:
                         
                         weights[i] = st.slider(f'Select weight for {sector}', min_value=1.0, max_value=100.0, value=1.0)
                         
                     i = i + 1
                     
                 col1, col2, col3 = st.columns(3)

                 with col1:
                     pass
                 with col3:
                     pass
                 with col2:
                     submit_button = st.form_submit_button(label='Run Monte Carlo')
                 
    else:

         pass
        
    
    if st.session_state.counter != 0:
        if st.session_state.counter != -1:
            counter = st.session_state.counter

    if counter != 0:
        
        if year_selectbox != '<none>':

                counter = -1





#############################################################################


    
if counter == -1:    #Run the monte carlo

              
        st.markdown("<h1 style='text-align: center; color: black;'>Monte Carlo</h1>", unsafe_allow_html=True)
        st.write('')
        st.markdown("<h1 style='text-align: center; color: black;'>Please Wait While Monte Carlo Runs</h1>", unsafe_allow_html=True)

        # Set timeframe to 1Day

        timeframe = '1D'

        # Format current date as ISO format

        end_date = datetime.datetime.now()
        end_date = int(round(end_date.timestamp())) * 1000  #<-- Convert datetime to milliseconds 
        end_date_str = str(end_date)
        end_date_str = end_date_str[:10]  #<-- This removes all but the last 10 millisecond values for the time which is format yahoo wants

        start_date_str = '345427200'
      

        tickers_and_data_df = pd.DataFrame()
        

        # Build Yahoo finance URL for the data request.
        
        i=0
        for sector in list_of_selected_sectors:

            if sector == '^VIX':
                    list_of_selected_sectors[i] = 'VIX'
                    #st.write(option[i][1])
            i=i+1
            
        i=0
        while i < 16:
            sector = option[i][1]
            if sector not in banned_ticker_list:
                
                single_ticker_df = functions.get_df_from_yahoo_finance_by_day(sector) #Make Yahoo data call based on selections
                tickers_and_data_df = pd.concat([tickers_and_data_df, single_ticker_df])
                
            i = i+1
            

        tickers_and_data_df = tickers_and_data_df.rename(columns={'Close': 'close'})
       
        # Manually concatenating data to shape it for monte carlo.  <-- TODO: Change this to dynamic
        
        VHT = tickers_and_data_df[tickers_and_data_df['Ticker']=='VHT'].drop('Ticker', axis=1).set_index('Date')
        XLE = tickers_and_data_df[tickers_and_data_df['Ticker']=='XLE'].drop('Ticker', axis=1).set_index('Date')
        QQQ = tickers_and_data_df[tickers_and_data_df['Ticker']=='QQQ'].drop('Ticker', axis=1).set_index('Date')
        BND = tickers_and_data_df[tickers_and_data_df['Ticker']=='BND'].drop('Ticker', axis=1).set_index('Date')
        XLI = tickers_and_data_df[tickers_and_data_df['Ticker']=='XLI'].drop('Ticker', axis=1).set_index('Date')
        VIX = tickers_and_data_df[tickers_and_data_df['Ticker']=='^VIX'].drop('Ticker', axis=1).set_index('Date')
        XLF = tickers_and_data_df[tickers_and_data_df['Ticker']=='XLF'].drop('Ticker', axis=1).set_index('Date')
        SHV = tickers_and_data_df[tickers_and_data_df['Ticker']=='SHV'].drop('Ticker', axis=1).set_index('Date')
        GLD = tickers_and_data_df[tickers_and_data_df['Ticker']=='GLD'].drop('Ticker', axis=1).set_index('Date')
        NFTUSD = tickers_and_data_df[tickers_and_data_df['Ticker']=='NFT-USD'].drop('Ticker', axis=1).set_index('Date')
        BTCUSD = tickers_and_data_df[tickers_and_data_df['Ticker']=='BTC-USD'].drop('Ticker', axis=1).set_index('Date')
        SPY = tickers_and_data_df[tickers_and_data_df['Ticker']=='SPY'].drop('Ticker', axis=1).set_index('Date')

        concat_df = pd.DataFrame()

        list_of_selected_sectors2 = list_of_selected_sectors.copy()
        

    
        for sector in list_of_selected_sectors2:
            
            if sector in banned_ticker_list:
                
                list_of_selected_sectors = list_of_selected_sectors2.remove(sector) 

             
        sector_list = str(list_of_selected_sectors2)
        separator = ", "
        sector_list_no_quotes = separator.join(list_of_selected_sectors2)
        sector_list_no_quotes = sector_list_no_quotes.replace('-','')
        build_df_string = 'portfolio = pd.concat([' + sector_list_no_quotes + '], axis=1, keys=' + sector_list + ').dropna()'       
        exec(build_df_string)


     
        
        weight_string = ''
        sum_weights = 0
      
        i=0
        while i < len(weights):

            sum_weights = sum_weights + weights[i]
            i=i+1
            
      
        i=0
        while i < len(weights):

            weights[i] = weights[i] / sum_weights
            weight_string = weight_string + ',' + str(weights[i])
            i = i+1
            

        i=0
        while i < len(weights):

            sum_weights = sum_weights + weights[i]
            i=i+1

            
        weight_string = weight_string[1:]

        mc_sim_string = 'mc30_year = MCSimulation(portfolio_data = portfolio, weights=[' + weight_string + '], num_simulation=100, num_trading_days=(252*year_selectbox))'
        exec(mc_sim_string) #Set parameters for monte carlo


        mc30_year.calc_cumulative_return() #calculate monte carlo
        MC_sim_dist_plot = mc30_year.plot_distribution()     
        MC_sim_line_plot = mc30_year.plot_simulation()
        MC_summary_statistics = mc30_year.summarize_cumulative_return()

        
        st.pyplot(MC_sim_line_plot.get_figure()) #Render monte carlo plots
        st.write('')

        col1, col2 = st.columns([2,6])

        with col1:
            st.write(MC_summary_statistics)
         
        with col2:
            st.pyplot(MC_sim_dist_plot.get_figure())
            
        st.markdown(f"<center>The following were used for this analysis: {sector_list_no_quotes}</center>", unsafe_allow_html=True)
                 
        col1, col2, col3, col4, col5 = st.columns(5)  #<-- This is how things are centered in Streamlit

        with col1:
            pass
        with col2:
            pass
        with col3:
            st.write('')
            st.button('Reset To Main', on_click=rerun_script)
        with col4:
            pass
        with col5:
            pass

        st.stop()
    
        


############################################################################
    

if counter != 0: #Get data if any boxes are checked
        
    
    if 'CC' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, consumer_confidence_df], axis=0)

    if 'CPI' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, cpi_df], axis=0)
        
    if 'M3' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, money_supply_df], axis=0)

    if 'Fed_Rates' in list_of_selected_sectors:

        tickers_and_data_df = pd.concat([tickers_and_data_df, long_term_fed_rates_df], axis=0)

     

    
    tickers_and_data_df['Change'] = tickers_and_data_df['Close'] - tickers_and_data_df['Close'].shift(-1)
    tickers_and_data_df['Pct_Change'] = tickers_and_data_df['Close'].pct_change()
    tickers_and_data_df['Date']=pd.to_datetime(tickers_and_data_df['Date'])
    tickers_and_data_df = tickers_and_data_df.drop_duplicates(subset=['Ticker', 'Date'], keep='last')

    dynamic_start = str(slider_range[0]) #<-- From sidebar date slider
    dynamic_end = str(slider_range[1])
    date_filter = (tickers_and_data_df['Date']>dynamic_start) & (tickers_and_data_df['Date'] <= dynamic_end)

    tickers_and_data_df = tickers_and_data_df.loc[date_filter]
    tickers_and_data_df_mc = tickers_and_data_df

    pivoted_tickers_and_data_df_ = tickers_and_data_df.pivot(index="Date", columns="Ticker")
    pivoted_tickers_and_data_df = pivoted_tickers_and_data_df_.dropna()
    pivoted_tickers_and_data_df2 = pivoted_tickers_and_data_df

    
    
#Run mckenzie test
    
    with st.sidebar:
        with st.expander("McKenzie Test", expanded=False):
            with st.form(key='mckenzie_selector'):
                
                st.markdown("<center><h1 style= text-align: center; color: black;>Please Select Asset for Mckenzie test</center>", unsafe_allow_html=True)
                col = st.columns(1)
               
                tick = st.text_input('Enter One Ticker', 'SPY')
               
                single_ticker_df_mc = functions.get_df_from_yahoo_finance(tick) #pull data from inputed ticker
                single_ticker_df_mc['Date']=pd.to_datetime(single_ticker_df_mc['Date'])
                single_ticker_df_mc['Date']=single_ticker_df_mc['Date'].dt.date
                single_ticker_df_mc['Pct_Change'] = single_ticker_df_mc['Close'].pct_change()
                tickers_and_data_df_mc['Date'] =pd.to_datetime(tickers_and_data_df_mc['Date'])                                  
                tickers_and_data_df_mc['Date']=tickers_and_data_df_mc['Date'].dt.date
                tickers_and_data_df_mc = tickers_and_data_df_mc.drop('Change', axis=1)  
                tickers_and_data_df_mc1 = pd.concat([tickers_and_data_df_mc, single_ticker_df_mc]) #combine df with data from main nav
                tickers_and_data_df_mc1['Date']= pd.to_datetime(tickers_and_data_df_mc1['Date'])
                tickers_and_data_df_mc1['Date'] = tickers_and_data_df_mc1['Date'].dt.date
                tickers_and_data_df_mc1 = tickers_and_data_df_mc1.drop_duplicates(subset=['Ticker', 'Date'], keep='last')   
                pivoted_tickers_and_data_df_mc = tickers_and_data_df_mc1.pivot(index="Date", columns="Ticker")
                pivoted_tickers_and_data_df_mc = pivoted_tickers_and_data_df_mc.dropna()
                pct_change_mc = pivoted_tickers_and_data_df_mc['Pct_Change']
                corr_df_mc = pct_change_mc.corr()                                                                           
                list_of_selected_sectors_mc = list_of_selected_sectors.copy()
                list_of_selected_sectors_mc.append(tick)
                submit_button = st.form_submit_button(label='Submit')
                sharpe_dict = functions.sharpe_ratio_calculator_original(list_of_selected_sectors_mc,pct_change_mc) #calculate sharpe ratio for all tickers in df
                result = functions.mckenzie_test(list_of_selected_sectors,tick,sharpe_dict, corr_df_mc)
                st.write(result)
                st.write('')
                
        col1, col2, col3 = st.columns(3)

        with col1:
            pass
        with col3:
            pass
        with col2:
            st.write('')
            st.button('Reboot App', on_click=rerun_script)

            
if counter == 0: #Welcome page - nothing checked

    st.markdown("<h1 style='text-align: center; color: black;'>Welcome To The Zoom Team 6 Correlation Analyzer</h1>", unsafe_allow_html=True)
    st.write()
    st.write('')
    st.markdown("<h0 style='text-align: center; color: black; font-size: 15pt;'>This application conducts correlation studies between economic sectors and various indices. \
                  Please select the indices you would like to study from the sidebar on the left.\
                  </h0>", unsafe_allow_html=True)
    

if counter == 2:  #<-- When only two items are selected, this head to head dashboard is displayed.

    st.markdown(f"<center><h0 style='text-align: center; color: black; font-size: 30pt;'>Comparison of {list_of_selected_sectors[0]} and {list_of_selected_sectors[1]}</center></h0>",unsafe_allow_html=True )

    # Row A

    a1, a2 = st.columns(2)

    with a1: #2 tickers selected  -- This is histogram of correlated periods

        #Render histogram for 2 ticker correlation analysis
        histogram_data_ = pivoted_tickers_and_data_df2['Pct_Change']
        histogram_data_['Correlation']  = histogram_data_[list_of_selected_sectors[0]].rolling(3).corr(histogram_data_[list_of_selected_sectors[1]])
        fig = plt.figure() 
        sns.histplot(data=histogram_data_, x='Correlation').set(title='Counts Of Correlated Periods')
        
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.
        

        
    with a2:  #2 tickers selected  -- This is bar plot of all periods by correlation

        #Render bar plot for 2 ticker correlation analysis
        
        histogram_data_['Correlation']  = histogram_data_[list_of_selected_sectors[0]].rolling(12).corr(histogram_data_[list_of_selected_sectors[1]])
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
        

    # Row B <---- Rolling Beta Graph
    
    b1 = st.columns(1)

    line_plot_data = {}
    pivoted_plot_data_df = {}
    line_plot_data = tickers_and_data_df[tickers_and_data_df['Ticker'].isin(list_of_selected_sectors)]


    if 'SPY' in list_of_selected_sectors:

        pass

    else:
        
        spy_data = functions.get_df_from_yahoo_finance('SPY')
        spy_data['Change'] = spy_data['Close'] - spy_data['Close'].shift(-1)
        spy_data['Pct_Change'] = spy_data['Close'].pct_change()
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

    
    bar_plot = []

    color = ['navy','turquoise','blue','limegreen','darkgreen','royalblue','green', 'black']
    sns.set()


    i=0
    for sector in list_of_selected_sectors:  #<-- Render beta barplot.  TODO: Fix Legend and Date
    
        bar_plot.append(sns.barplot(data=rolling_beta, x='Date', y=sector, color=color[i]))
        
        i = i + 1
    
    plt.xlabel("Date")
    plt.ylabel("βeta")
    plt.title("βeta Of Selected Sectors") # You can comment this line out if you don't need title
    st.write(fig)
        
    # Row C <----- Sharpe Ratio Graph
    
    pct_change_sharpe_ratio_graph = pivoted_tickers_and_data_df2['Pct_Change']
    c1 = st.columns(1)
    sd = functions.sharpe_ratio_calculator(list_of_selected_sectors,pct_change_sharpe_ratio_graph)
    sd=sd.loc[[0]]
    sd = sd.T # manipulate dictionary to allow it to be read by altair
    sd = sd.reset_index()
    sd.columns =['Ticker','Sharpe']
    bar_chart_sharpe = alt.Chart(sd).mark_bar().encode(x='Ticker',y='Sharpe',).properties(title='Sharpe Ratios')
    st.altair_chart(bar_chart_sharpe, use_container_width=True)
    

if counter > 2:

    
    st.markdown(f"<center><h0 style='text-align: center; color: black; font-size: 30pt;'>Multi Sector Comparison</center></h0>",unsafe_allow_html=True )
      
    # Row A <------ Correlation Heat Map

    a1, a2= st.columns(2)

    with a1:

        
        fig = plt.figure()
        correlation_heatmap = sns.heatmap(pivoted_tickers_and_data_df['Pct_Change'].corr(), annot = True, cmap="YlGnBu")
        plt.title("Sector Correlation Heatmap", fontsize=20)
                                          
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.
        
    with a2:

        plot_data = pivoted_tickers_and_data_df['Pct_Change']
        plot_data = plot_data.unstack(level=-1)
        plot_data = plot_data.reset_index()
        plot_data.columns = ['Ticker', 'Date', 'Value']
        
        
        fig = plt.figure() 
        box_plot = sns.boxplot(x= plot_data['Ticker'], y=plot_data['Value'], palette="Blues")  #<-- Render box plot
        plt.title("Sector Volatility", fontsize=20)

        
        buffer_ = BytesIO()                     #Strange workaround for image sizing in streamlit.
        fig.savefig(buffer_, format="png")      #Saves plot as image 
        st.image(buffer_)                       #Writes image instead of rendering plot, making charts scale properly.


    # Row B  <-- Rolling beta plot

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
    

    fig = plt.figure() #Render rolling beta chart.
    bar_plot = []
    color = ['navy','turquoise','blue','limegreen','darkgreen','royalblue','green', 'black', 'yellow', 'orange', 'gray']
    sns.set()

    i=0
    for sector in list_of_selected_sectors:
    
        bar_plot.append(sns.barplot(data=rolling_beta, x='Date', y=sector, color=color[i]))
        i = i + 1

    plt.xlabel("Date")
    plt.ylabel("βeta")
    plt.title("βeta Of Selected Sectors") 
    st.write(fig)


    # Row C <------- Sharpe Ratio Graph
    
    
    pct_change_sharpe_ratio_graph = pivoted_tickers_and_data_df2['Pct_Change'] #Render Sharp Ratio Bar Chart
    c1 = st.columns(1)
    sd = functions.sharpe_ratio_calculator(list_of_selected_sectors,pct_change_sharpe_ratio_graph)
    sd = sd.loc[[0]]
    sd = sd.T # manipulate dictionary to allow it to be read by altair
    sd = sd.reset_index()
    sd.columns =['Ticker','Sharpe']
    bar_chart_sharpe = alt.Chart(sd).mark_bar().encode(x='Ticker',y='Sharpe',).properties(title='Sharpe Ratios')
    st.altair_chart(bar_chart_sharpe, use_container_width=True)
    
    
