# file to sort the comparisons between a claim and evidence retrieved for that claim - sorts article judgement
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sentence_comparison as sentence_comparison

class evidence_sentence_comparison():
    # this class needs to store a url and the claim for the url
    # get the article text from that url
    # run claim detection on that article text
    # take the top 3 claims made in the article
    # run a comparison between the stored claim and each extracted claim
    # come to a judgement on the article and return that judgement with comparison scores
    def __init__(self, url, claim):
        load_dotenv()
        self.url = url
        self.claim = claim
        self.article = ''
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']
        self.sentence_comparison_object = sentence_comparison.sentence_comparison()
        self.top_claims = []
        self.sorted_top_claims = []
        self.judgements = ""
        self.ranked_sentences = {}

    # runs the article judgement process
    def run(self):
        self.get_article_text()
        self.claim_detection()
        top_claims = self.get_top_claims()
        self.get_judgement(top_claims)
        return self.judgements

    # get article text from url
    def get_article_text(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_body = soup.find('article')
            if article_body:
                paragraphs = article_body.find_all('p')
                for paragraph in paragraphs:
                    self.article += paragraph.text

    # run claim detection on article text of evidence
    def claim_detection(self):
        self.processed_html = self.article.replace(".", ". ")
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{self.processed_html}"
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            self.ranked_sentences = api_response.json()
            return self.ranked_sentences
        else:
            print(f"Request failed with status code: {api_response.status_code}")

    # method to get the top claims ranked in a piece of text
    def get_top_claims(self):
        results = self.ranked_sentences.get("results")
        if results:
            for result in results:
                if result.get("score") > 0.5:
                    self.top_claims += [result]
            self.sorted_top_claims = sorted(self.top_claims, key=lambda x: x['score'])
        return self.top_claims[:5]

    # determining overall judgement of a piece of evidence compared to a claim
    def get_judgement(self, top_claims):
        # need judgement of each top claim
        agree = 0
        disagree = 0
        for claim in top_claims:
            judgement = self.sentence_comparison_object.sentences_agree(self.claim, claim['text'])
            if judgement['agreement'] == "agree":
                agree += 1
            elif judgement['agreement'] == "disagree":
                disagree += 1
        if agree > disagree:
            self.judgements = "agree"
        elif disagree > agree:
            self.judgements = "disagree"
        else:
            self.judgements = "no judgement"

