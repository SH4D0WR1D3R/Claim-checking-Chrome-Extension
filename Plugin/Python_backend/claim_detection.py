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
    ranked_sentences = {}

    def __init__(self):
        load_dotenv()
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']
    
    # set the pure article html for the active tab
    def set_article_html(self, html):
        self.article_html = html
    
    # get the pure article html for the active tab
    def get_article_html(self):
        return self.article_html
    
    # get all article sentences that have been ranked based on how worthy they are of being checked
    def get_ranked_sentences(self):
        return self.ranked_sentences
    
    # method to take the html of the article and return a string of sentences of the article text
    def filter_article_html(self):
        # TO DO: check if file exists
        with open(self.html_file_name, "r", encoding="utf-8") as temp_html_file:
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
    
    # method to rank the sentences from the article
    def filter_sentences(self):
        self.processed_html = self.processed_html.replace(".", ". ") # to ensure it works with the API being used
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{self.processed_html}"
        # TO DO: should do a check on sentences
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            self.ranked_sentences = api_response.json()
            # print("SENTENCES ", self.ranked_sentences)
            return self.ranked_sentences
        else:
            print(f"Request failed with status code: {api_response.status_code}")

    def convert_to_file(self):
        # check if file already exists? 
        # TO DO: if no article_html to write, make sure to delete html_file.html if it exists
        open(self.html_file_name, "w").close() # clear file
        with open(self.html_file_name, "w", encoding="utf-8") as html_file:
            html_file.write(self.article_html)

    # from the sentences that have been given a rate, filter out any that are below 0.5
    def find_top_sentences(self):
        # print("RESULTS ", self.ranked_sentences.get("results"))
        results = self.ranked_sentences.get("results")
        top_results = []
        if results:
            for result in results:
                # TO DO: want to change to just be top 3
                if result.get("score") > 0.7:
                    top_results += [result]

        # print("TOP RESULTS ", top_results)
        return top_results
    
    def test_similarity_score(self, claimA, claimB):
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/claim_similarity/simple_similarity/score/claim_a/{claimA}/claim_b/{claimB}"
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            similarity_score = api_response.json()
            # print("SIMILARITY SCORE ", similarity_score)
            return similarity_score
        else:
            print(f"Request failed with status code: {api_response.status_code}")


# testing of methods
# temp_object = claim_detection()
# temp_object.filter_sentences("the earth is flat. donald trump is banned from running in 2 states.")
# temp_object = claim_detection()
# temp_object.test_similarity_score("England is a country", "The grass is green")