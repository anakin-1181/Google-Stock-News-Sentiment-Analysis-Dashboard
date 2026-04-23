from datetime import datetime, timedelta
from urllib.parse import quote
from zoneinfo import ZoneInfo

import feedparser
import pandas as pd

from .massive_client import MassiveClient

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
        if df.empty:
            raise ValueError(f"No recent news headlines found for {self.tick}.")
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
    
class MassiveStockScrapper:
    def __init__(self, tick):
        self.tick = tick.strip().upper()
        self.client = MassiveClient()

    def _fetch_from_massive(self, period: str) -> pd.DataFrame:
        days = int(period.removesuffix("d")) if period.endswith("d") else 7
        today = datetime.now(tz=ZoneInfo("America/New_York")).date()
        start_date = today - timedelta(days=max(days * 3, 14))

        bars = self.client.get_daily_bars(
            ticker=self.tick,
            start_date=start_date.isoformat(),
            end_date=today.isoformat(),
        )
        if not bars:
            raise ValueError(
                f"No recent Massive price data found for {self.tick}. Massive stock pricing is U.S.-market focused."
            )

        df = pd.DataFrame.from_records(bars)
        df["Date"] = (
            pd.to_datetime(df["t"], unit="ms", utc=True)
            .dt.tz_convert("America/New_York")
            .dt.tz_localize(None)
            .dt.normalize()
        )
        df = df.rename(columns={"c": "Close"})
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.loc[:, ["Date", "Close"]].dropna(subset=["Close"])
        df = df.loc[df["Date"] >= pd.Timestamp(start_date), :]
        if df.empty:
            raise ValueError(f"No recent Massive closing prices found for {self.tick}.")
        return df.set_index("Date").sort_index()

    def fetch_stock_data(self, period="7d") -> pd.DataFrame:
        return self._fetch_from_massive(period=period)
    
    def process_dataframe(self) -> pd.DataFrame:
        # Only need "Date" and "Close" columns
        df = self.fetch_stock_data()
        if len(df) < 2:
            raise ValueError("Not enough price data found")
        else:
            df["Close"] = df["Close"].round(2)
            df = df.loc[:, ["Close"]].reset_index().assign(Date=lambda x: x["Date"].dt.date)    
            df["Daily_return (%)"] = round(df["Close"].pct_change() * 100, 2)
            df["Date"] = pd.to_datetime(df["Date"])
            return df
        
        
