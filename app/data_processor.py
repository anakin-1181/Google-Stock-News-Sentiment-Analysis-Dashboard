from .data_scrapper import GoogleNewsScrapper, YFinanceScrapper
from .sentiment_analyser import SentimentDfGenerator
import pandas as pd
import yfinance as yf

class DataProcessor:
    def __init__(self, tick, company_name):
        self.tick = tick
        self.company_name = company_name

    def _remove_duplicate_titles(self, df: pd.DataFrame) -> pd.DataFrame:
        if "Title" not in df.columns:
            return df

        dedup_df = df.copy()
        dedup_df["_title_key"] = (
            dedup_df["Title"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.lower()
        )
        dedup_df = dedup_df.drop_duplicates(subset=["_title_key"]).drop(columns=["_title_key"])
        return dedup_df.reset_index(drop=True)
        
    def generate_sentiment_df(self):
        # Prepare news headline dataframe
        headline_scrapper = GoogleNewsScrapper(tick=self.tick, company_name=self.company_name)
        input_df = headline_scrapper.generate_dataframe()
        input_df = self._remove_duplicate_titles(input_df)
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
        self.ticker = ticker.strip().upper()
        
    def ticker_to_company_name(self):
        try:
            stock = yf.Ticker(ticker=self.ticker)
            if stock.history(period="5d").empty:
                raise ValueError("No stock data found")

            try:
                info = stock.info
                return info.get("longName") or info.get("shortName") or self.ticker
            except Exception:
                return self.ticker
        except Exception as e:
            print(e)
            raise Exception
