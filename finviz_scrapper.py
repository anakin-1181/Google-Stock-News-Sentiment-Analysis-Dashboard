from bs4 import BeautifulSoup
import requests
import pandas as pd

def fetch_url(tick: str):
    """_summary_

    Args:
        tick: Company tick

    Returns:
        html code of the news-table element
    """
    full_url = "https://finviz.com/quote.ashx?t=" + tick
    response = requests.get(full_url, headers={"User-Agent": "my-app"})
    soup = BeautifulSoup(response.content, "html.parser")
    html_data = soup.find(id="news-table")
    return html_data

def parse_html_to_df(html_data) -> pd.DataFrame:
    table_rows = html_data.find_all("tr")
    list_of_parsed_rows = []
    for index, row in enumerate(table_rows):
        title = row.a.text
        if len(row.td.text.split()) > 1:
            date = row.td.text.split()[0]
            timestamp = row.td.text.split()[1]
        parsed_row = {"Date":date, "Timestamp": timestamp, "Title":title}
        list_of_parsed_rows.append(parsed_row)
    return pd.DataFrame.from_dict(list_of_parsed_rows)

if __name__ == "__main__":
    nvda_df = parse_html_to_df(fetch_url("NVDA"))
    print(nvda_df)
    