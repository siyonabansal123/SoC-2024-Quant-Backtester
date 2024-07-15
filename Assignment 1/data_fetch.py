
import yfinance as yf
import pandas as pd

def download_historical_data(symbol: str, start_date: str, end_date: str, timeframe: str = '1d') -> pd.DataFrame:
        data = yf.download(symbol, start=start_date, end=end_date, interval=timeframe)
        print(data)
        return data
    


