import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.data_processor import DataProcessor, TickerParser
from app.data_analyser import DataAnalyser
from io import StringIO
import sys

# Page setup
st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")

st.title("📊 Stock Sentiment Analysis Dashboard")
st.markdown("*Analyze the relationship between news sentiment and stock returns*")

# ==================== Navigation side bar ====================
st.sidebar.header("📍 Navigation")
page = st.sidebar.radio(
    "Jump to section:",
    ["🔍 Analyze", "📊 Dataframes", "📈 Graphs"],
    index=0
)

st.sidebar.divider()

# Input section in sidebar
st.sidebar.header("⚙️ Settings")
input_tick = st.sidebar.text_input("Enter stock ticker:", value="AAPL")

# Analyze button
analyze_button = st.sidebar.button("🔍 Run Analysis", type="primary")

st.sidebar.divider()
st.sidebar.caption("Use navigation above to jump between sections")

# ==================== Initial State ====================
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'dp' not in st.session_state:
    st.session_state.dp = None
if 'da' not in st.session_state:
    st.session_state.da = None
if 'sentiment_df' not in st.session_state:
    st.session_state.sentiment_df = None
if 'logs' not in st.session_state:
    st.session_state.logs = ""

# ==================== Analyze button logic ====================
if analyze_button:
    captured_output = StringIO()
    sys.stdout = captured_output
    
    with st.spinner("Running analysis..."):
        try:
            print("Starting analysis...", "\n")
            tp = TickerParser(ticker=input_tick)
            company_name = tp.ticker_to_company_name()
            
            # Initialize processors
            st.session_state.dp = DataProcessor(tick=input_tick, company_name=company_name)
            st.session_state.da = DataAnalyser(tick=input_tick, company_name=company_name)
            st.session_state.sentiment_df = st.session_state.dp.generate_sentiment_df()[0]
            
            st.session_state.analyzed = True
            
            print("\n","Analysis complete!")
            st.success("Analysis completed successfully!")
            
        except Exception as e:
            st.error(f"Please input a valid company ticker.")
            st.session_state.analyzed = False
            
        finally:
            sys.stdout = sys.__stdout__
            st.session_state.logs = captured_output.getvalue()

# ==================== Analyzed Pages ====================
if not st.session_state.analyzed:
    st.info("👈 Enter a stock ticker and click 'Run Analysis' to begin")
    
else:
    # Page 1: Analyze Overview
    if page == "🔍 Analyze":
        st.header("🔍 Analysis Overview")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Stock Ticker", input_tick)
        with col2:
            st.metric("Company", company_name)
        with col3:
            corr = st.session_state.da.df['normalised_STM_Score'].corr(
                st.session_state.da.df['normalised_Daily_return'])
            st.metric("Correlation between Sentiment Score and Daily Return", f"{corr:.3f}")
            
        
        st.divider()
        
        # Summary
        st.subheader("📋 Summary")
        if st.session_state.da.df is not None:
            
            st.markdown(f"""
            - **Date Range:** {st.session_state.da.df['Date'].min()} to {st.session_state.da.df['Date'].max()}
            - **Total News Articles Analyzed:** {len(st.session_state.sentiment_df)}
            """)
        
        st.divider()
        
        # Logs
        st.subheader("📋 Output Log")
        st.text_area("", value=st.session_state.logs, height=150, label_visibility="collapsed")
    
    # Page 2: Dataframes
    elif page == "📊 Dataframes":
        st.header("📊 Data Tables")
        
        # Sentiment Data
        st.subheader("1. News Sentiment Analysis")
        st.markdown("*Individual sentiment scores for each news headline*")
        st.dataframe(st.session_state.sentiment_df, use_container_width=True, height=300)
        
        # Download button
        csv = st.session_state.sentiment_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sentiment Data as CSV",
            data=csv,
            file_name=f"{input_tick}_sentiment_data.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # Normalized Data
        st.subheader("2. Normalized Data")
        st.markdown("*Sentiment scores and daily returns normalized using Z-scores*")
        st.dataframe(st.session_state.da.df, use_container_width=True, height=300)
        
        # Download button
        csv2 = st.session_state.da.df.to_csv(index=False)
        st.download_button(
            label="📥 Download Normalized Data as CSV",
            data=csv2,
            file_name=f"{input_tick}_normalized_data.csv",
            mime="text/csv"
        )
    
    # Page 3: Graphs
    elif page == "📈 Graphs":
        st.header("📈 Visualizations")
        
        # Update plot sizes dynamically
        # Time Series
        st.subheader("1. Time Series Comparison")
        st.caption("Track how sentiment and returns change over time")
        
        # Create plot with custom size
        plt.style.use("seaborn-v0_8-darkgrid")
        fig1, ax1 = plt.subplots(figsize=(12,6), dpi=100)
        
        df = st.session_state.da.df
        x = df.index
        ax1.plot(x, df["normalised_STM_Score"], color="tab:orange", marker="o", label="normalised sentiment score")
        ax1.plot(x, df["normalised_Daily_return"], color="tab:blue", marker="o", label="normalised daily return")
        ax1.set_title(f"Sentiment Score vs Daily Return ({input_tick})")
        ax1.set_xticks(df.index)
        ax1.set_xticklabels(df["Date"])
        ax1.tick_params(axis="x", labelrotation=45)
        ax1.legend()
        plt.tight_layout()
        
        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)
        
        st.divider()
        
        # Scatter Plot
        st.subheader("2. Correlation Analysis")
        st.caption("Examine the relationship between sentiment scores and daily returns")
        
        from scipy.stats import pearsonr
        import seaborn as sns
        
        sns.set_theme()
        fig2, ax2 = plt.subplots(figsize=(12,6), dpi=100)
        
        stm_score = df["normalised_STM_Score"]
        daily_return = df["normalised_Daily_return"]
        corr, p_val = pearsonr(stm_score, daily_return)
        
        sns.regplot(x=stm_score, y=daily_return, ax=ax2, ci=None)
        ax2.text(0.05, 0.95, f'r = {corr:.3f}', 
                transform=ax2.transAxes, 
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax2.set_title(f"Sentiment Score vs Daily Return ({input_tick})")
        ax2.set_ylabel("Daily Return")
        ax2.set_xlabel("Sentiment Score")
        plt.tight_layout()
        
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)
        
        st.divider()
        
        # Bar Chart
        st.subheader("3. Side-by-Side Comparison")
        st.caption("Compare normalized sentiment and returns for each day")
        
        fig3, ax3 = plt.subplots(figsize=(12,6), dpi=100)
        df[["normalised_STM_Score", "normalised_Daily_return"]].plot(
            kind="bar", ax=ax3, color=["tab:orange", "tab:blue"]
        )
        ax3.set_title(f"Sentiment Score vs Daily Return ({input_tick})")
        ax3.legend(["normalised sentiment score", "normalised daily return"])
        ax3.set_xticklabels(df["Date"])
        plt.tight_layout()
        
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)