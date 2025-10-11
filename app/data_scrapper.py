import feedparser
import pandas as pd
import yfinance as yf
from datetime import datetime
from urllib.parse import quote

class GoogleNewsScrapper:
    def __init__(self, tick, company_name):
        self.tick = tick
        self.company_name = company_name
        
    def _fetch_data(self) -> pd.DataFrame:
        query = f"{self.tick} OR {self.company_name} when:7d" # Grab recent data from last week
        encoded_query = quote(query)

        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return pd.DataFrame.from_dict(feed.entries)
    
    def generate_dataframe(self):
        df = self._fetch_data()
        df = df.loc[:, ["published", "title"]]
        df.columns = ["Date", "Title"]
        df["Date"] = pd.to_datetime(df["Date"])
        df["Day"] = df["Date"].dt.day_name()
        df["is_weekday"] = ((df["Day"] != "Saturday") & (df["Day"] != "Sunday"))
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        df["Source"] = df["Title"].apply(lambda x: x.rsplit("-",1)[1])
        df["Title"] = df["Title"].apply(lambda x: x.rsplit("-",1)[0])
        df = df[["Date","Day", "Source", "Title", "is_weekday"]]
        return df
    
class YFinanceScrapper:
    def __init__(self, tick):
        self.tick = tick
        
    def fetch_stock_data(self, period="7d") -> pd.DataFrame:
        stock = yf.Ticker(ticker=self.tick)
        return stock.history(period=period)
    
    def process_dataframe(self) -> pd.DataFrame:
        # Only need "Date" and "Close" columns
        df = self.fetch_stock_data()
        if len(df) < 7:
            raise Exception 
        else:
            df["Close"] = df["Close"].round(2)
            df = df.loc[:, ["Close"]].reset_index().assign(Date=lambda x: x["Date"].dt.date)    
            df["Daily_return (%)"] = round(df["Close"].pct_change() * 100, 2)
            df["Date"] = pd.to_datetime(df["Date"])
            return df
        
        