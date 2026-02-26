import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import zscore
from scipy.stats import pearsonr
from .data_processor import DataProcessor

class DataAnalyser:
    figsize = (12,6)
    
    def __init__(self, tick, company_name):
        self.tick = tick
        self.company_name = company_name
        self.df = self._prepare_dataframe()
        
    def _normalise_cols(self, df:pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["normalised_STM_Score"] = zscore(df["STM Score"]).round(2)
        df["normalised_Daily_return"] = zscore(df["Daily_return (%)"]).round(2)
        return df
    
    def _prepare_dataframe(self):
        dp = DataProcessor(tick=self.tick, company_name=self.company_name)
        df = dp.generate_full_df() 
        df["Date"] = df["Date"].dt.date
        return self._normalise_cols(df)
        
        
    def plot_time_series(self):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.df["Date"],
                y=self.df["normalised_STM_Score"],
                mode="lines+markers",
                name="normalised sentiment score",
                line=dict(color="#ff7f0e"),
                marker=dict(size=8),
                hovertemplate="Date: %{x}<br>Sentiment: %{y}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=self.df["Date"],
                y=self.df["normalised_Daily_return"],
                mode="lines+markers",
                name="normalised daily return",
                line=dict(color="#1f77b4"),
                marker=dict(size=8),
                hovertemplate="Date: %{x}<br>Daily Return: %{y}<extra></extra>",
            )
        )
        fig.update_layout(
            title=f"Sentiment Score vs Daily Return ({self.tick})",
            xaxis_title="Date",
            yaxis_title="Normalised Value",
            template="plotly_white",
            hovermode="x unified",
        )
        return fig
        
    def plot_scatter(self):
        stm_score = self.df["normalised_STM_Score"]
        daily_return = self.df["normalised_Daily_return"]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=stm_score,
                y=daily_return,
                mode="markers",
                name="data points",
                marker=dict(color="#ff7f0e", size=10, opacity=0.9, line=dict(color="#ffffff", width=1)),
                text=self.df["Date"].astype(str),
                hovertemplate="Date: %{text}<br>Sentiment: %{x}<br>Daily Return: %{y}<extra></extra>",
            )
        )

        if len(self.df) > 1:
            slope, intercept = np.polyfit(stm_score, daily_return, 1)
            x_line = np.linspace(stm_score.min(), stm_score.max(), 100)
            y_line = slope * x_line + intercept
            fig.add_trace(
                go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode="lines",
                    name="trend line",
                    line=dict(color="#d62728", dash="dash"),
                    hoverinfo="skip",
                )
            )

            corr, _ = pearsonr(stm_score, daily_return)
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=0.02,
                y=0.98,
                text=f"r = {corr:.3f}",
                showarrow=False,
                font=dict(color="#ffffff", size=14),
                bgcolor="rgba(0, 0, 0, 0.75)",
                bordercolor="#ff7f0e",
                borderwidth=1,
                borderpad=6,
            )

        fig.update_layout(
            title=f"Sentiment Score vs Daily Return ({self.tick})",
            xaxis_title="Sentiment Score",
            yaxis_title="Daily Return",
            template="plotly_white",
        )
        return fig
        
    def plot_bar_charts(self):
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=self.df["Date"],
                y=self.df["normalised_STM_Score"],
                name="normalised sentiment score",
                marker_color="#ff7f0e",
                hovertemplate="Date: %{x}<br>Sentiment: %{y}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Bar(
                x=self.df["Date"],
                y=self.df["normalised_Daily_return"],
                name="normalised daily return",
                marker_color="#1f77b4",
                hovertemplate="Date: %{x}<br>Daily Return: %{y}<extra></extra>",
            )
        )
        fig.update_layout(
            title=f"Sentiment Score vs Daily Return ({self.tick})",
            xaxis_title="Date",
            yaxis_title="Normalised Value",
            barmode="group",
            template="plotly_white",
        )
        return fig
        
        
        
    
    

    
    
        
    
        
    
    
    
    
