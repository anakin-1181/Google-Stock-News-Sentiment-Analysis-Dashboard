from .data_scrapper import GoogleNewsScrapper, YFinanceScrapper
from .sentiment_analyser import SentimentDfGenerator
import pandas as pd
import yfinance as yf

class DataProcessor:
    def __init__(self, tick, company_name):
        self.tick = tick
        self.company_name = company_name
        
    def generate_sentiment_df(self):
        # Prepare news headline dataframe
        headline_scrapper = GoogleNewsScrapper(tick=self.tick, company_name=self.company_name)
        input_df = headline_scrapper.generate_dataframe()
        # Process news headline dataframe with sentiment analyser
        stm_analyser = SentimentDfGenerator()
        analysed_df = stm_analyser.generate_analysed_df(df=input_df)
        # Process analysed_df groupped by date
        summary_df = stm_analyser.generate_summary_df(df=analysed_df)
        return analysed_df, summary_df
    
    def _format_df(self, df:pd.DataFrame) -> pd.DataFrame:
        return df.dropna(subset=["Close"]).reset_index(drop=True)
        
    
    def generate_full_df(self):
        # Prepare stock data from yf
        yf_scrapper = YFinanceScrapper(tick=self.tick)
        stock_df = yf_scrapper.process_dataframe()
        summary_df = self.generate_sentiment_df()[1]
        # Merge df 
        merged_df = summary_df.merge(stock_df, on="Date", how="left")
        merged_df["Date"] = pd.to_datetime(merged_df["Date"])
        # Remove weekends and current day
        return self._format_df(merged_df)
        
class TickerParser:
    def __init__(self, ticker):
        self.ticker = ticker
        
    def ticker_to_company_name(self):
        try:
            stock = yf.Ticker(ticker=self.ticker)
            return stock.info["longName"]
        except Exception as e:
            print(e)
            raise Exception