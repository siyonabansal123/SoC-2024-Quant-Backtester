# performance.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_closing_prices(data: pd.DataFrame ):

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price', color = "green")
    plt.title('Stock Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid(True)
    plt.show()
