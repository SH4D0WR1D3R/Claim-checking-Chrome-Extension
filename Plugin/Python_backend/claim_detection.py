# make classes
# think through how is the article going to be passed into this?

# will use the API for claimbuster for now

from dotenv import load_dotenv
import requests
import json
import os
from bs4 import BeautifulSoup

class claim_detection:
    article_html = None
    processed_html = None
    html_file_name = "html_file.html"

    def __init__(self):
        load_dotenv()
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']
    
    # Method to set the html document to the variable article_html
    # intention is for article_html to be the html of the webpage currently open
    def set_article_html(self, html):
        self.article_html = html
    
    def get_article_html(self):
        return self.article_html
    
    # method to take the html of the article and return a string of sentences of the article text
    # beautiful soup
    # probably need to store the html string in a file
    def filter_article_html(self):
        # check if file exists
        with open(self.html_file_name, "r") as temp_html_file:
            html_content = temp_html_file.read()

        html_soup = BeautifulSoup(html_content, 'html.parser')
        title = html_soup.find('title').get_text()
        article_content = ''
        article_body = html_soup.find('article')
        if article_body:
            paragraphs = article_body.find_all('p')
            for paragraph in paragraphs:
                article_content += paragraph.text

        self.processed_html = article_content
        return title, article_content
    
    # method to take an input of a bunch of sentences and return those sentences with ratings of importance as a claim/to be verified
    # have now realised might not be good to use this
    # will continue to use this but it doesn't have the focus i'd like
    # /api/v2/score/text/sentences/<input_text> - input text is a block of text, where sentences are separated by full stop
    def filter_sentences(self):
        # sentences needs to be a string to be passed into the api endpoint
        # so assume sentences is a string type and not a file type
        self.processed_html = self.processed_html.replace(".", ". ") # to ensure it works with the API being used
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{self.processed_html}"
        # should do a check on sentences
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            data = api_response.json()
            return data
        else:
            print(f"Request failed with status code: {api_response.status_code}")


    def convert_to_file(self):
        # check if file already exists? 
        html_file = open(self.html_file_name, "w")
        html_file.write(self.article_html)
        html_file.close()

    

# testing of methods
# temp_object = claim_detection()
# temp_object.filter_sentences("the earth is flat. donald trump is banned from running in 2 states.")