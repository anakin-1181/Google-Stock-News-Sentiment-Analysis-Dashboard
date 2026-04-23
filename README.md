# Google Stock News Sentiment Analysis Dashboard

An interactive web application that aims to answer the question: **"Does news headline of the company affect stock performance?"**

This dashboard fetches recent news articles from Google News RSS feed, performs sentiment analysis using FinBERT from huggingface, and visualizes the correlation with daily stock returns to explore the relationship between media sentiment and market movements.

![Dashboard Preview](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗%20Hugging%20Face-FinBERT-yellow?style=for-the-badge)

## Research Background

This project ponders the question **"Does news headline of the company affect stock performance?"** by investigating whether publicly available news sentiment has predictive power for stock returns. 

**Key Questions:**
- Do markets efficiently incorporate news sentiment?
- Is there a lag between sentiment and price movements?
- Does the strength of correlation vary by company or sector?



## Features

- **Real-time News Scraping**: Fetches latest news articles from Google News RSS feeds
- **AI-Powered Sentiment Analysis**: Utilizes FinBERT model from Hugging Face for financial sentiment classification
- **Stock Data Integration**: Retrieves historical stock prices from Yahoo Finance
- **Interactive Visualizations**: 
  - Time series comparison of sentiment vs returns
  - Correlation scatter plots with trend lines
  - Side-by-side bar chart comparisons
- **Multi-page Navigation**: Clean interface with separate pages for analysis, data tables, and graphs
- **Data Export**: Download analysed data as CSV files

## Demo

[Live Demo (https://ssd-anakin1181.streamlit.app)](https://ssd-anakin1181.streamlit.app)


### 1. Analyse
- Overview metrics (ticker, company name, correlation)
- Summary statistics
- Analysis output logs

### 2. Dataframes
- News sentiment analysis table
- Normalized summary data
- CSV export functionality

### 3. Graphs
- Time series comparison
- Correlation scatter plot
- Side-by-side bar charts

## How It Works

1. **Data Collection**
   - Fetches news articles (max 100) from Google News RSS feed for the past 7 days
   - Retrieves stock price data from Yahoo Finance

2. **Sentiment Analysis**
   - analyses sentiment of each news headline using **FinBERT** (Financial BERT model from Hugging Face)
   - FinBERT is specifically trained on financial texts for accurate sentiment classification
   - Calculates daily average sentiment scores
   - Scores range from -1 (negative) to +1 (positive)

3. **Data Processing**
   - Merges sentiment data with stock returns
   - Filters weekdays only (excludes weekends when markets are closed)
   - Normalizes data using Z-scores for fair comparison

4. **Visualization**
   - Plots time series trends
   - analyses correlation between sentiment and returns
   - Provides multiple visualization perspectives

## Sample Analysis

**Research Question:** Does news headline sentiment affect stock performance?

**Input:** `AAPL` (Apple Inc.)

**Output:**
- Correlation coefficient between sentiment and returns
- 7-day trend visualization
- Daily sentiment scores and stock returns
- Statistical summary

**Interpretation:**
- Positive correlation suggests news sentiment may influence returns
- Negative correlation suggests contrarian market behavior
- Near-zero correlation suggests weak relationship



