from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .data_scrapper import GoogleNewsScrapper
import torch
import pandas as pd
import math

class SentimentAnalyser:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    
    def tokenize_text(self, text):
        return self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    def analyze_sentiment(self, texts):
        with torch.no_grad():
            input_tokens = self.tokenize_text(texts)
            outputs = self.model(**input_tokens)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return probs.tolist()

class SentimentDfGenerator:
        
    def _generate_score_col(self, row: pd.Series):
        pos, neg, neu = row["Positive"], row["Negative"], row["Neutral"]
        # If the probability of positive and negative tone is too close then return 0.0 (neutral)
        if neu > 0.8 or abs(pos-neg) < 0.1:
            return 0.0
        else:
            return round(pos-neg, 2)
            

    def generate_analysed_df(self,df: pd.DataFrame, batch_size=20) -> pd.DataFrame:
        # Batch sentiment analysis
        titles = df.loc[:, "Title"].tolist()
        all_predictions = []
        
        stm_analyser = SentimentAnalyser()
        for i in range(0, len(titles), batch_size):
            print(f"Processing {i}/{len(titles)} batch...")
            batch = titles[i : i+batch_size]
            cur_pred = stm_analyser.analyze_sentiment(batch)
            all_predictions.extend(cur_pred) # Add each item to all_predictions
            
        # Add prediction to dataframe    
        df = df.copy()
        df["Positive"] = [round(pred[0],2) for pred in all_predictions]
        df["Negative"] = [round(pred[1],2) for pred in all_predictions]
        df["Neutral"] = [round(pred[2],2) for pred in all_predictions]
        df["STM Score"] = df.apply(self._generate_score_col, axis=1)
        df["Date"] = df["Date"].dt.date
        return df
    
    def generate_summary_df(self, df):
        pt = df.pivot_table(index=["Date", "Day"], values=["STM Score", "is_weekday"], aggfunc="mean").reset_index()
        pt["STM Score"] = pt["STM Score"].round(2)
        pt["Date"] = pd.to_datetime(pt["Date"])
        return pt
        


if __name__ == "__main__":
    with pd.option_context('display.max_colwidth', None, 'display.max_columns', None,):
        stm_df_generator = SentimentDfGenerator()
        df = stm_df_generator.generate_summary_df()
        
    
    
