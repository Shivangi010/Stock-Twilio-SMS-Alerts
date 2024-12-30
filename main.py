import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

STOCK_API_KEY = ""
NEWS_API_KEY = ""

stock_params = {
"function":"TIME_SERIES_DAILY",
"symbol": STOCK_NAME,
"apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
#print(yesterday_data)
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)


day_before_yesterday_data = data_list[1]
#print(day_before_yesterday_data)
day_before_yesterday_price_data = float(day_before_yesterday_data["4. close"])
print(day_before_yesterday_price_data)



positive_absolute_diff = float(yesterday_closing_price)-float(day_before_yesterday_price_data)
up_down = None
if positive_absolute_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(positive_absolute_diff)

percentage_diff = round(abs(positive_absolute_diff/float(yesterday_closing_price))*100)
# real_percentage_diff= round((percentage_diff),2)
print(percentage_diff)


if abs(percentage_diff)  >1:
#print("Get News")
   news_param = {
     "apiKey" : NEWS_API_KEY,
     "q": COMPANY_NAME,
    # "language": "en",
    # "pageSize" : "5"
        }

response = requests.get(NEWS_ENDPOINT, params=news_param)
articles = response.json()["articles"]

three_articles = articles[:3]
print(three_articles)


formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadlines: {article["title"]}. \nBrief: {article["description"]}" for article in three_articles]



client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_="+",
        to="+"
    )

