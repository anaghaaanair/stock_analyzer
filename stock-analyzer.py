#imports
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob

#getting the news
newsapi=NewsApiClient(api_key="8a42d009131b479583cf91334e7fa514")

#starting page
print("==============================================")
print("Stock Analyzer📈")
print("==============================================")

#ask user to enter ticker
ticker=input("Enter ticker: ")

#news
news=newsapi.get_everything(
    q=ticker,
    language="en",
    sort_by="publishedAt",
    page_size=5
)

#stock data period
stock=yf.Ticker(ticker)
data=stock.history(period="6mo")

#get closing prices
close_prices=data["Close"]

#calculate daily returns
returns=close_prices.pct_change()
average_return=returns.mean()
volatility=returns.std()

#range of the returns
highest=close_prices.max()
lowest=close_prices.min()
current=close_prices.iloc[-1]


#printing everything
print()
print("Stock:", ticker.upper())
print(f"Current price: ${current:.2f}")
print(f"Highest price: ${highest:.2f}")
print(f"Lowest price: ${lowest:.2f}")
print(f"Average Daily Return: {average_return*100:.2f}%")
print(f"Volatility: {volatility*100:.2f}%")

#sentiment codes
score=0
print("\nLatest news:\n")

for article in news["articles"]:
    title=article["title"]
    print("•", title)
    sentiment=TextBlob(title).sentiment.polarity
    score+=sentiment

#scoring the news
print()
if score>0:
    print("Overall sentiment: Positive")
elif score<0:
    print("Overall sentiment: Negative")
else:
    print("Overall sentiment: Neutral")

#graphically present
plt.figure(figsize=(10, 5))
plt.plot(close_prices)
plt.title(f"{ticker.upper()} Stock Price")
plt.xlabel("Date")
plt.ylabel("Price in $")
plt.grid()
plt.show()