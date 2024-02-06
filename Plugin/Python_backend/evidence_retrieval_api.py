
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['NEWS_API_KEY'] # doesn't like api key for some reason
print(api_key)

query = "Thousands"
endpoint_url = f"https://newsapi.org/v2/everything?q={query}&apiKey=api_key"
request_headers = {"x-api-key": api_key}
api_response = requests.get(url=endpoint_url, headers=request_headers)
print(api_response.json())