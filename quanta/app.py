from flask import Flask, render_template, request
import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Route to handle user queries
@app.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    user_question = request.form['user_question']
    answer = process_question(user_question)

    return render_template('index.html', question=user_question, answer=answer)
    #return render_template('index.html', question=user_question, answer=answer)

def get_historical_price_graph(symbol, period='1mo'):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)


def process_question(question):
    # Clean and process the question
    question = question.lower()

    # Initialize response variable
    answer = ""

    # Parse the question and determine what the user is asking
    if "current price of" in question:
        symbol = question.split("current price of ")[1].upper()
        answer = get_current_price(symbol)
    elif "compare the price of" in question:
        symbols = question.split("compare the price of ")[1].split(" and ")
        answer = compare_prices(symbols)
    elif "closing price of" in question:
        symbol = question.split("closing price of ")[1].upper()
        answer = get_closing_price_today(symbol)
    elif "price of" in question and "yesterday" in question:
        symbol = question.split("price of ")[1].split(" yesterday")[0].upper()
        answer = get_price_yesterday(symbol)
    elif "price of" in question and "one month ago" in question:
        symbol = question.split("price of ")[1].split(" one month ago")[0].upper()
        answer = get_price_one_month_ago(symbol)
    elif "highest price of" in question and "last month" in question:
        symbol = question.split("highest price of ")[1].split(" in the last month")[0].upper()
        answer = get_highest_price_last_month(symbol)
    elif "about" in question:
        symbol = question.split("about ")[1].upper()
        answer = get_basic_info(symbol)
    elif "sector is" in question:
        symbol = question.split("sector is ")[1].upper()
        answer = get_sector(symbol)
    elif "industry does" in question:
        symbol = question.split("industry does ")[1].split(" belong to")[0].upper()
        answer = get_industry(symbol)
    elif "market cap of" in question:
        symbol = question.split("market cap of ")[1].upper()
        answer = get_market_cap(symbol)
    elif "how many employees" in question:
        symbol = question.split("how many employees ")[1].upper()
        answer = get_employees(symbol)
    elif "latest news" in question:
        symbol = question.split("latest news about ")[1].upper()
        answer = get_latest_news(symbol)
    elif "summarize the latest news about" in question:
        symbol = question.split("summarize the latest news about ")[1].upper()
        answer = get_news_summary(symbol)
    elif "good time to buy" in question:
        symbol = question.split("good time to buy ")[1].upper()
        answer = get_investment_advice(symbol)
    elif "should i sell my" in question:
        symbol = question.split("should i sell my ")[1].split(" shares")[0].upper()
        answer = get_investment_advice(symbol, sell=True)
    elif "top performing stocks" in question:
        answer = get_top_performing_stocks()
    elif "how is the stock market doing" in question:
        answer = get_market_overview()
    elif "trend for tech stocks" in question:
        answer = get_tech_stock_trend()
    elif "current value of the s&p 500" in question:
        answer = get_index_value('^GSPC')
    elif "how is nasdaq performing" in question:
        answer = get_index_value('^IXIC')
    elif "impact of the latest earnings report on" in question:
        symbol = question.split("impact of the latest earnings report on ")[1].upper()
        answer = get_earnings_report_impact(symbol)
    elif "p/e ratio of" in question:
        symbol = question.split("p/e ratio of ")[1].upper()
        answer = get_pe_ratio(symbol)
    elif "dividend yield of" in question:
        symbol = question.split("dividend yield of ")[1].upper()
        answer = get_dividend_yield(symbol)
    else:
        answer = "Sorry, I don't understand the question."


    return answer


def get_current_price(symbol):
    stock = yf.Ticker(symbol)
    current_price = stock.history(period='1d')['Close'].iloc[-1]
    return f"The current price of {symbol} is ${current_price:.2f}"


def compare_prices(symbols):
    try:
        comparisons = []
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            current_price = stock.history(period='1d')['Close'].iloc[-1]
            one_month_ago_price = stock.history(period='1mo')['Close'].iloc[0]
            price_change = ((current_price - one_month_ago_price) / one_month_ago_price) * 100
            market_cap = stock.info.get('marketCap', 'N/A')
            pe_ratio = stock.info.get('trailingPE', 'N/A')
            comparisons.append({
                'symbol': symbol,
                'current_price': current_price,
                'one_month_ago_price': one_month_ago_price,
                'price_change': price_change,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio
            })

        response = ""
        for comp in comparisons:
            response += (f"{comp['symbol']}:\n"
                         f"  Current Price: ${comp['current_price']:.2f}\n"
                         f"  Price One Month Ago: ${comp['one_month_ago_price']:.2f}\n"
                         f"  Price Change: {comp['price_change']:.2f}%\n"
                         f"  Market Cap: ${comp['market_cap']:,}\n"
                         f"  P/E Ratio: {comp['pe_ratio']}\n\n")
        return response.strip()
    except IndexError:
        return "Could not retrieve the necessary data for the given symbols."


def get_closing_price_today(symbol):
    stock = yf.Ticker(symbol)
    closing_price = stock.history(period='1d')['Close'].iloc[-1]
    return f"The closing price of {symbol} today was ${closing_price:.2f}"


def get_price_yesterday(symbol):
    stock = yf.Ticker(symbol)
    yesterday = stock.history(period='2d')['Close'].iloc[-2]
    return f"The price of {symbol} yesterday was ${yesterday:.2f}"


def get_price_one_month_ago(symbol):
    stock = yf.Ticker(symbol)
    one_month_ago = stock.history(period='1mo')['Close'].iloc[0]
    return f"The price of {symbol} one month ago was ${one_month_ago:.2f}"


def get_highest_price_last_month(symbol):
    stock = yf.Ticker(symbol)
    last_month_high = stock.history(period='1mo')['High'].max()
    return f"The highest price of {symbol} in the last month was ${last_month_high:.2f}"


def get_basic_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return f"{info['longName']} ({symbol}) is in the {info['sector']} sector and {info['industry']} industry."


def get_sector(symbol):
    stock = yf.Ticker(symbol)
    return f"{symbol} is in the {stock.info['sector']} sector."


def get_industry(symbol):
    stock = yf.Ticker(symbol)
    return f"{symbol} belongs to the {stock.info['industry']} industry."


def get_market_cap(symbol):
    stock = yf.Ticker(symbol)
    market_cap = stock.info['marketCap']
    return f"The market cap of {symbol} is ${market_cap:.2f}"


def get_employees(symbol):
    stock = yf.Ticker(symbol)
    employees = stock.info['fullTimeEmployees']
    return f"{symbol} has {employees} employees."


def get_latest_news(symbol):
    stock = yf.Ticker(symbol)
    news = stock.news
    return f"Latest news for {symbol}: {news[0]['title']} - {news[0]['link']}"


def get_news_summary(symbol):
    stock = yf.Ticker(symbol)
    news = stock.news
    return f"Summary of the latest news for {symbol}: {news[0]['title']} - {news[0]['summary']}"


def get_investment_advice(symbol, sell=False):
    stock = yf.Ticker(symbol)
    if sell:
        advice = (f"It's difficult to give specific investment advice, but consider consulting a financial advisor "
                  f"about selling {symbol} shares.")
    else:
        advice = (f"It's difficult to give specific investment advice, but consider consulting a financial advisor "
                  f"about buying {symbol} shares.")
    return advice


def get_top_performing_stocks():
    # This is a placeholder implementation
    return "Top performing stocks: AAPL, MSFT, TSLA, AMZN, GOOGL."


def get_market_overview():
    # This is a placeholder implementation
    return "The stock market is experiencing mixed performance today."


def get_tech_stock_trend():
    # This is a placeholder implementation
    return "Tech stocks are trending upwards this week."


def get_index_value(index_symbol):
    stock = yf.Ticker(index_symbol)
    current_value = stock.history(period='1d')['Close'].iloc[-1]
    return f"The current value of {index_symbol} is ${current_value:.2f}"


def get_earnings_report_impact(symbol):
    # This is a placeholder implementation
    return f"The latest earnings report had a positive impact on {symbol}."


def get_pe_ratio(symbol):
    stock = yf.Ticker(symbol)
    pe_ratio = stock.info['trailingPE']
    return f"The P/E ratio of {symbol} is {pe_ratio:.2f}"


def get_dividend_yield(symbol):
    stock = yf.Ticker(symbol)
    dividend_yield = stock.info['dividendYield']
    return f"The dividend yield of {symbol} is {dividend_yield:.2%}"


if __name__ == '__main__':
    app.run(debug=True)
