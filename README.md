# Google Stock News Sentiment Analysis Dashboard

An interactive web application that aims to answer the question: **"Does news headline of the company affect stock performance?"**

This dashboard fetches recent news articles from Google News RSS feed, performs sentiment analysis using FinBERT from huggingface, and visualizes the correlation with daily stock returns to explore the relationship between media sentiment and market movements.

![Dashboard Preview](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗%20Hugging%20Face-FinBERT-yellow?style=for-the-badge)

## 🌟 Features

- **Real-time News Scraping**: Fetches latest news articles from Google News RSS feeds
- **AI-Powered Sentiment Analysis**: Utilizes FinBERT model from Hugging Face for financial sentiment classification
- **Stock Data Integration**: Retrieves historical stock prices from Yahoo Finance
- **Interactive Visualizations**: 
  - Time series comparison of sentiment vs returns
  - Correlation scatter plots with trend lines
  - Side-by-side bar chart comparisons
- **Multi-page Navigation**: Clean interface with separate pages for analysis, data tables, and graphs
- **Data Export**: Download analysed data as CSV files

## 🚀 Demo

[Live Demo (https://ssd-anakin1181.streamlit.app)](https://ssd-anakin1181.streamlit.app)

## 📋 Prerequisites

- Python 3.12 or higher
- pip or uv (Python package manager)

## 🔧 Installation

### Option 1: Using uv (Recommended)

This project uses [uv](https://github.com/astral-sh/uv) for fast dependency management.

1. **Install uv**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

### Option 2: Using pip

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit pandas matplotlib seaborn scipy yfinance feedparser numpy transformers torch
   ```

## 📦 Dependencies

This project is managed using `pyproject.toml`:

```toml
[project]
name = "finance-sentiment-analyser"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "feedparser>=6.0.12",
    "matplotlib>=3.10.7",
    "numpy>=2.3.3",
    "pandas>=2.3.3",
    "requests>=2.32.5",
    "scipy>=1.16.2",
    "seaborn>=0.13.2",
    "streamlit>=1.50.0",
    "torch>=2.8.0",
    "transformers>=4.57.0",
    "yfinance>=0.2.66",
]
```

**Key Libraries:**
- **transformers** - Hugging Face library for FinBERT model
- **torch** - PyTorch backend for model inference
- **streamlit** - Web application framework
- **yfinance** - Yahoo Finance data retrieval
- **feedparser** - RSS feed parsing for news articles

## 🎯 Usage

1. **Run the application locally**
   ```bash
   streamlit run dashboard.py
   ```

2. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8501`

3. **analyse a stock**
   - Enter a stock ticker (e.g., AAPL, NVDA, TSLA) in the sidebar
   - Click "Run Analysis"
   - Navigate between different pages to view results

## 🎨 Dashboard Pages

### 1. 🔍 analyse
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

## 📊 Sample Analysis

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

## 🤖 About FinBERT

This project uses [FinBERT](https://huggingface.co/ProsusAI/finbert), a pre-trained NLP model specifically designed for financial sentiment analysis. FinBERT is a BERT-based model fine-tuned on financial communication texts, making it particularly effective at understanding sentiment in financial news headlines.

**Model Features:**
- Fine-tuned on financial phrasebank and analyst reports
- Classifies text into positive, negative, or neutral sentiment
- State-of-the-art performance on financial sentiment tasks
- Available through Hugging Face Transformers library

## Acknowledgments

- [Streamlit](https://streamlit.io/) - Web framework
- [Hugging Face](https://huggingface.co/) - FinBERT model and Transformers library
- [yfinance](https://github.com/ranaroussi/yfinance) - Stock data
- [Google News RSS](https://news.google.com/) - News articles
- [ProsusAI/FinBERT](https://huggingface.co/ProsusAI/finbert) - Financial sentiment analysis model

## Known Issues

- Analysis limited to past 7 days due to Google News RSS constraints
- Weekend data is filtered out (no stock trading)
- First run may be slow due to FinBERT model download (~400MB)
- Sentiment analysis accuracy depends on headline quality and financial context


## Research Background

This project ponders the question **"Does news headline of the company affect stock performance?"** by investigating whether publicly available news sentiment has predictive power for stock returns. 

**Key Questions:**
- Do markets efficiently incorporate news sentiment?
- Is there a lag between sentiment and price movements?
- Does the strength of correlation vary by company or sector?

