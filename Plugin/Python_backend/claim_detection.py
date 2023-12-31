# make classes
# think through how is the article going to be passed into this?

# will use the API for claimbuster for now

from dotenv import load_dotenv
import requests
import json
import os

class claim_detection:
    article_html = None
    processed_html = None

    def __init__(self):
        load_dotenv()
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']
    
    # Method to set the html document to the variable article_html
    # intention is for article_html to be the html of the webpage currently open
    def set_article_html(self, html):
        self.article_html = html
    
    def get_article_html(self):
        return self.article_html
    
    
    def filter_html(self):
        return None
    
    # method to take an input of a bunch of sentences and return those sentences with ratings of importance as a claim/to be verified
    # have now realised might not be good to use this
    # will continue to use this but it doesn't have the focus i'd like
    # /api/v2/score/text/sentences/<input_text> - input text is a block of text, where sentences are separated by full stop
    def filter_sentences(self, sentences):
        # sentences needs to be a string to be passed into the api endpoint
        # so assume sentences is a string type and not a file type
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{sentences}"
        # should do a check on sentences
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            data = api_response.json()
            print(data)
        else:
            print(f"Request failed with status code: {api_response.status_code}")

temp_object = claim_detection()
temp_object.filter_sentences("the earth is flat. donald trump is banned from running in 2 states.")