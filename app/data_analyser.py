import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
import seaborn as sns
from scipy.stats import pearsonr
from .data_processor import DataProcessor
import matplotlib.pyplot as plt

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
        plt.style.use("seaborn-v0_8-darkgrid")
        
        print(self.df)
        
        fig, ax = plt.subplots(figsize=DataAnalyser.figsize, dpi=100)
        x = self.df.index
        date = self.df["Date"]
        stm_score = self.df["normalised_STM_Score"]
        daily_return = self.df["normalised_Daily_return"]

        ax.plot(x, stm_score, color="tab:orange", marker="o", label="normalised sentiment score")
        ax.plot(x, daily_return, color="tab:blue", marker="o", label="normalised daily return")

        ax.set_title(f"Sentiment Score vs Daily Return ({self.tick})")

        # plt.axhline(y=0, color='black', linewidth=1)
        ax.set_xticks(self.df.index)
        ax.set_xticklabels(date)
        # ax.tick_params(axis="x", labelrotation=45)
        ax.legend()
        plt.tight_layout()
        return fig
        
    def plot_scatter(self):
        sns.set_theme()
        
        fig, ax = plt.subplots(figsize=DataAnalyser.figsize, dpi=100)
        
        x = self.df.index
        date = self.df["Date"]
        stm_score = self.df["normalised_STM_Score"]
        daily_return = self.df["normalised_Daily_return"]
        corr, p_val = pearsonr(stm_score,daily_return)
    
        
        sns.regplot(x=stm_score, y=daily_return, ax=ax, ci=None)
        
        ax.text(0.05, 0.95, f'r = {corr:.3f}', 
            transform=ax.transAxes, 
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(f"Sentiment Score vs Daily Return ({self.tick})")
        ax.set_ylabel("Daily Return")
        ax.set_xlabel("Sentiment Score")
        return fig
        
    def plot_bar_charts(self):
        fig, ax = plt.subplots(figsize=DataAnalyser.figsize, dpi=100)
        
        self.df[["normalised_STM_Score", "normalised_Daily_return"]].plot(kind="bar", ax=ax, color=["tab:orange", "tab:blue"])
        
        ax.set_title(f"Sentiment Score vs Daily Return ({self.tick})")
        ax.legend(["normalised sentiment score", "normalised daily return"])
        ax.set_xticklabels(self.df["Date"])
        ax.tick_params(axis="x", labelrotation=0)
        
        return fig
        
        
        
    
    

    
    
        
    
        
    
    
    
    