# StonksBot

![Logos](/logo/logos.png)

This is a Discord bot developed by Dion Osvaldo Hananto to fulfill the requirements of a stock-related Discord bot. The bot is built using Python and utilizes the `discord.py` library. It provides various functionalities related to stock trading and is specifically designed for the Indonesian stock market.

## Features

1. Displaying stock charts: The bot can display charts of stock prices upon request.
2. Trading plan management: Users can save their trading plans, including automatic cut-loss targets.
3. Trading hour reminders: The bot can send reminders to users regarding trading hours based on the Indonesian stock market schedule.
4. Company name lookup: Given a stock ticker code, the bot can provide detailed information about the corresponding company.
5. ARA and ARB calculations: The bot can calculate ARA (Auto-Rejection Area) and ARB (Auto-Rejection Buy) limits.
6. Stock-related news: The bot provides real-time stock-related news by scraping data from relevant websites.
7. LQ45 stock categorization: The bot can identify stocks categorized under LQ45.
8. Crypto coin prices: When the stock market is closed, the bot can display real-time cryptocurrency prices as the status on Discord.
9. Crypto price tracking: The bot can track and record price movements of cryptocurrencies.
10. IPO ticker detection: The bot can automatically retrieve data for newly listed IPO tickers in the Indonesian stock market.

## Usage Limitation

The usage of this bot is limited & restricted to authorized individuals only.

## Security

To ensure security, not everyone is allowed to create trade plans. Only authorized administrators have the privilege to create trade plans.

## Real-time Data

Real-time stock data for Indonesian stocks is obtained through web scraping using Puppeteer (JavaScript). Web scraping is the process of extracting data from websites programmatically. This approach is taken to avoid the high costs associated with using the official API provided by the Indonesian Stock Exchange (BEI).

Real-time cryptocurrency prices are obtained from the Binance API.

Stock-related news is fetched by scraping data from relevant online websites. The bot retrieves the latest news articles related to stocks and provides them to the users.

The bot is also capable of automatically fetching data for newly listed IPO tickers in the Indonesian stock market, ensuring that users have access to the latest information.

## Technology Stack

- Python: The bot is built using Python programming language.
- Discord.py: The `discord.py` library is used for interacting with the Discord API.
- JavaScript: Puppeteer is utilized for web scraping of real-time stock data and news.
- JSON: The bot utilizes JSON as the database for storing data.