# 📊 Stock Sentiment Analysis Dashboard

An interactive web application that analyzes the relationship between news sentiment and stock market returns. This dashboard fetches recent news articles, performs sentiment analysis, and visualizes the correlation with daily stock returns.

![Dashboard Preview](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)

## 🌟 Features

- **Real-time News Scraping**: Fetches latest news articles from Google News RSS feeds
- **Sentiment Analysis**: Analyzes sentiment of news headlines using NLP
- **Stock Data Integration**: Retrieves historical stock prices from Yahoo Finance
- **Interactive Visualizations**: 
  - Time series comparison of sentiment vs returns
  - Correlation scatter plots with trend lines
  - Side-by-side bar chart comparisons
- **Multi-page Navigation**: Clean interface with separate pages for analysis, data tables, and graphs
- **Data Export**: Download analyzed data as CSV files
- **Real-time Logs**: Monitor analysis progress with output logs

## 🚀 Demo

[Live Demo](https://your-app-url.streamlit.app) *(Add your deployed URL here)*

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Requirements

Create a `requirements.txt` file with the following:

```txt
streamlit>=1.28.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.11.0
yfinance>=0.2.28
feedparser>=6.0.10
numpy>=1.24.0
```

## 🎯 Usage

1. **Run the application locally**
   ```bash
   streamlit run dashboard.py
   ```

2. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8501`

3. **Analyze a stock**
   - Enter a stock ticker (e.g., AAPL, NVDA, TSLA) in the sidebar
   - Click "Run Analysis"
   - Navigate between different pages to view results

## 📁 Project Structure

```
stock-sentiment-analysis/
│
├── dashboard.py              # Main Streamlit application
│
├── app/
│   ├── data_processor.py     # Data processing and merging logic
│   ├── data_analyser.py      # Visualization and analysis
│   ├── data_scrapper.py      # News and stock data scraping
│   ├── sentiment_analyser.py # Sentiment analysis implementation
│   └── ...
│
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
└── .gitignore               # Git ignore file
```

## 🎨 Dashboard Pages

### 1. 🔍 Analyze
- Overview metrics (ticker, company name, correlation)
- Summary statistics
- Analysis output logs

### 2. 📊 Dataframes
- News sentiment analysis table
- Normalized summary data
- CSV export functionality

### 3. 📈 Graphs
- Time series comparison
- Correlation scatter plot
- Side-by-side bar charts

## 🔬 How It Works

1. **Data Collection**
   - Fetches news articles from Google News RSS feed for the past 7 days
   - Retrieves stock price data from Yahoo Finance

2. **Sentiment Analysis**
   - Analyzes sentiment of each news headline
   - Calculates daily average sentiment scores
   - Scores range from -1 (negative) to +1 (positive)

3. **Data Processing**
   - Merges sentiment data with stock returns
   - Filters weekdays only
   - Normalizes data using Z-scores

4. **Visualization**
   - Plots time series trends
   - Analyzes correlation between sentiment and returns
   - Provides multiple visualization perspectives

## 📊 Sample Analysis

**Input:** `AAPL` (Apple Inc.)

**Output:**
- Correlation coefficient between sentiment and returns
- 7-day trend visualization
- Daily sentiment scores and stock returns
- Statistical summary

