import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.data_processor import DataProcessor, TickerParser
from app.data_analyser import DataAnalyser
from io import StringIO
import sys

# Page setup
st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")

st.title("Stock News Sentiment Analysis Dashboard")
st.markdown("*This project ponders the question* **'Does news headline of the company affect stock performance?'** *by investigating whether news sentiment has predictive power for stock returns*")

# ==================== Navigation side bar ====================
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Jump to section:",
    ["Analyse", "Data Tables", "Graphs"],
    index=0
)
st.sidebar.divider()

# Input section in sidebar
st.sidebar.header("Settings")
input_tick = st.sidebar.text_input("Enter stock ticker:", value=st.session_state.get('input_tick', ''))
    
# analyse button
analyse_button = st.sidebar.button("Run Analysis", type="primary")

st.sidebar.divider()

# Supported Tickers
with st.sidebar.expander("Supported Tickers"):
    st.markdown("""
    **US Stocks (No suffix needed):**
    - `AAPL` - Apple
    - `MSFT` - Microsoft
    - `TSLA` - Tesla
    
    **International Stocks (Add suffix):**
    - `.L` - London (e.g., `BARC.L`)
    - `.TO` - Toronto (e.g., `SHOP.TO`)
    - `.T` - Tokyo (e.g., `7203.T`)
    - `.HK` - Hong Kong (e.g., `0700.HK`)
    - `.PA` - Paris (e.g., `AIR.PA`)
    - `.DE` - Frankfurt (e.g., `BMW.DE`)
    
    ⚠️ **Note:** Not all stocks are available.
    Delisted or very small companies may not work.
    """)
    
st.sidebar.divider()

st.sidebar.caption("Use navigation above to jump between sections")

# ==================== Initial State ====================
if 'analysed' not in st.session_state:
    st.session_state.analysed = False
if 'dp' not in st.session_state:
    st.session_state.dp = None
if 'da' not in st.session_state:
    st.session_state.da = None
if 'sentiment_df' not in st.session_state:
    st.session_state.sentiment_df = None
if 'company_name' not in st.session_state: 
    st.session_state.company_name = ""
if 'input_tick' not in st.session_state:  
    st.session_state.input_tick = ""


# ==================== analyse button logic ====================
if analyse_button:
    captured_output = StringIO()
    sys.stdout = captured_output
    
    with st.spinner("Running analysis..."):
        try:
            print("Starting analysis...", "\n")
            tp = TickerParser(ticker=input_tick)
            company_name = tp.ticker_to_company_name()
            
            st.session_state.company_name = company_name 
            st.session_state.input_tick = input_tick  
            
            # Initialize processors
            st.session_state.dp = DataProcessor(tick=st.session_state.input_tick, company_name=st.session_state.company_name)
            st.session_state.da = DataAnalyser(tick=st.session_state.input_tick, company_name=st.session_state.company_name)
            st.session_state.sentiment_df = st.session_state.dp.generate_sentiment_df()[0]
            
            st.session_state.analysed = True
            
            print("\n","Analysis complete!")
            st.success("Analysis completed successfully!")
            
        except Exception as e:
            st.error(f"Please input a valid company ticker.")
            st.session_state.analysed = False

# ==================== analysed Pages ====================
if not st.session_state.analysed:
    st.info("Enter a stock ticker and click 'Run Analysis' to begin")
    
else:
    # Page 1: analyse Overview
    if page == "Analyse":
        st.header("Analysis Overview")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Stock Ticker", st.session_state.input_tick)
        with col2:
            st.metric("Company", st.session_state.company_name)
        with col3:
            corr = st.session_state.da.df['normalised_STM_Score'].corr(
                st.session_state.da.df['normalised_Daily_return'])
            st.metric("Correlation between Sentiment Score and Daily Return", f"{corr:.3f}")
            
        
        st.divider()
        
        # Summary
        st.subheader("Summary")
        if st.session_state.da.df is not None:
            
            st.markdown(f"""
            - **Date Range:** {st.session_state.da.df['Date'].min()} to {st.session_state.da.df['Date'].max()}
            - **Total News Articles analysed:** {len(st.session_state.sentiment_df)}
            """)
        
        st.divider()
    
    # Page 2: Dataframes
    elif page == "Data Tables":
        st.header("Data Tables")
        
        # Sentiment Data
        st.subheader("1. News Sentiment Analysis")
        st.markdown("*Individual sentiment scores for each news headline*")
        display_df1 = st.session_state.sentiment_df.reset_index(drop=True).drop(columns=["is_weekday"])
        st.dataframe(display_df1, use_container_width=True, height=300)
        
        # Download button
        csv = st.session_state.sentiment_df.to_csv(index=False)
        st.download_button(
            label="Download Sentiment Data as CSV",
            data=csv,
            file_name=f"{input_tick}_sentiment_data.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # Summary Data
        st.subheader("2. Summary Data")
        st.markdown("*Summary data for the past weekdays*")
        st.markdown("""
                - **Sentiment Score: -1 (Negative) ~ 1 (Positive)**
                - **Daily Return (%): -100 ~ 100**
                """)
        display_df2 = st.session_state.da.df.drop(columns=["is_weekday"])
        display_df2 = display_df2[["Date", "Day", "STM Score", "normalised_STM_Score", "Daily_return (%)", "normalised_Daily_return"]]
        display_df2.columns = ["Date", "Day", "Sentiment Score", "nSentiment Score", "Daily Return (%)", "nDaily Return (%)"]
        st.dataframe(display_df2, use_container_width=True, height=300)
        
        # Download button
        csv2 = st.session_state.da.df.to_csv(index=False)
        st.download_button(
            label="Download Normalized Data as CSV",
            data=csv2,
            file_name=f"{input_tick}_normalized_data.csv",
            mime="text/csv"
        )
    
    # Page 3: Graphs
    elif page == "Graphs":
        st.header("Visualizations")
        
        # Time Series line graph
        
        st.subheader("1. Time Series Comparison")
        st.caption("Track how sentiment and returns change over time")
        
        st.pyplot(st.session_state.da.plot_time_series(), use_container_width=True)
        
        st.divider()
        
        # Scatter Plot
        st.subheader("2. Correlation Analysis")
        st.caption("Examine the relationship between sentiment scores and daily returns")
        
        st.pyplot(st.session_state.da.plot_scatter(), use_container_width=True)
        
        st.divider()
        
        # Bar Chart
        st.subheader("3. Side-by-Side Comparison")
        st.caption("Compare normalized sentiment and returns for each day")
        
        st.pyplot(st.session_state.da.plot_bar_charts(), use_container_width=True)