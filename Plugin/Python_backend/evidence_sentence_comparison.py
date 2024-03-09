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
        self.url = url
        self.claim = claim
        self.article = ''
        load_dotenv()
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']
        self.sentence_comparison_object = sentence_comparison.sentence_comparison()
        self.top_claims = []
        self.sorted_top_claims = []
        self.judgements = []
        self.ranked_sentences = {}

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
            # article_content = ''
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

    def get_top_claims(self):
        results = self.ranked_sentences.get("results")
        # top_results = []
        lowest_score = 1
        if results:
            for result in results:
                ## WORK ON 
                if result.get("score") > 0.5:
                    self.top_claims += [result]
            # sorted_list = sorted(list_of_dicts, key=lambda x: x['age'])
            self.sorted_top_claims = sorted(self.top_claims, key=lambda x: x['score'])
            print("SORTED TOP CLAIMS ", self.sorted_top_claims)
        return self.top_claims[:5]

    def get_judgement(self, top_claims):
        # need judgement of each top claim
        for claim in top_claims:
            judgement = self.sentence_comparison_object.sentences_agree(self.claim, claim['text'])
            self.judgements.append({claim['text']:judgement})
        # not sure what to do here to get a judgement on a piece of evidence


# object = evidence_sentence_comparison("https://www.theguardian.com/business/video/2023/dec/30/extreme-flooding-in-tunnel-used-by-eurostar-halts-trains-video", "A video taken inside the flooded tunnel shows water gushing onto the tracks from a pipe attached to the tunnel's wall.")
# print(object.run())

