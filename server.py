
from fastmcp import FastMCP
import asyncio
import json
import logging
import yfinance as yf
# Create an MCP server
mcp = FastMCP("Yahoo Finance MCP Server")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@mcp.tool()
def search_news(keyword: str) -> str:
    """Simulate news search using a ticker and return top articles."""
    stock = yf.Ticker(keyword.upper())
    news = stock.news[:5]
    result = []
    for article in news:
        result.append({
            "title": article.get("title"),
            "publisher": article.get("publisher"),
            "link": article.get("link"),
            "providerPublishTime": article.get("providerPublishTime"),
        })
    return json.dumps(result, indent=2)

@mcp.tool()
def get_ticker_info(ticker: str) -> str:
    stock = yf.Ticker(ticker)
    logger.info(f"getting info for {ticker} : {stock}")
    return json.dumps(stock.info, ensure_ascii=False)

@mcp.tool()
def get_ticker_news(ticker: str) -> str:
    stock = yf.Ticker(ticker)
    news = stock.news
    news = stock.news[:5]  # Top 5 articles
    result = []
    for article in news:
        result.append({
            "title": article.get("title"),
            "publisher": article.get("publisher"),
            "link": article.get("link"),
            "providerPublishTime": article.get("providerPublishTime"),
        })
    return json.dumps(result, indent=2)

@mcp.tool()
def search_quote(ticker: str) -> str:
    """Return the current stock price for a ticker."""
    stock = yf.Ticker(ticker)
    price = stock.info.get("regularMarketPrice")
    result = {
        "ticker": ticker.upper(),
        "price": price
    }
    return json.dumps(result, indent=2)

@mcp.tool()
def analyze_ticker(ticker: str) -> str:
    """Summarize key financial metrics and analysis for a given ticker."""
    stock = yf.Ticker(ticker)
    info = stock.info
    result = {
        "name": info.get("longName", ticker.upper()),
        "price": info.get("regularMarketPrice", "N/A"),
        "trailingPE": info.get("trailingPE", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "marketCap": info.get("marketCap", "N/A")
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def income_statement(stock_ticker: str) -> str:
    dat = yf.Ticker(stock_ticker)
    return str(f"Background information for {stock_ticker} {dat.quarterly_income_stmt}")

#async def main():
    #await mcp.run_http_async(host="0.0.0.0", port=8003, log_level="debug", path="/mcp")
    #mcp.run(transport="stdio") 

if __name__ == "__main__":
   #asyncio.run(main())
   mcp.run(transport="stdio") 