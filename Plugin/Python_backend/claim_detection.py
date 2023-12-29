# make classes
# think through how is the article going to be passed into this?

# will use the API for claimbuster for now

from dotenv import load_dotenv
import requests

class claim_detection:
    article_html = None
    processed_html = None

    def __init__(self, api_key):
        self.api_key = api_key
        load_dotenv()
    
    # Method to set the html document to the variable article_html
    # intention is for article_html to be the html of the webpage currently open
    def set_article_html(self, html):
        self.article_html = html
    
    def get_article_html(self):
        return self.article_html
    
    # method to take an input of a bunch of sentences and return those sentences with ratings of importance as a claim/to be verified
    # have now realised might not be good to use this
    # will continue to use this but it doesn't have the focus i'd like
    # /api/v2/score/text/sentences/<input_text> - input text is a block of text, where sentences are separated by full stop
    def filter_sentences(self):
        return None