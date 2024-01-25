# Module to handle retrieving evidence based on a claim or set of claims

# needs to do a google search essentially - can use the google-search module - python module
# 2 options for searching
    # - search for the exact claim - LETS GO WITH THIS FOR NOW
    # - search for the topics broken down from the claim
# probably better to search for exact claim but need to figure out about results - will need to break claim into topics anyways
# once the search has been executed, a topic check should be done against article headlines
# if topics match (unsure how to go about this since how many topics do we want matching?), that can be given to the user as a piece of evidence
# claims will need to be extracted from each article found and compared with the original claim

# will be handling this one problem at a time
# first create class
# then create function that takes a claim and searches for it exactly 

# ERROR: googlesearch isn't recognised
# from googlesearch import search
# from transformers import pipeline

# class evidence_retrieval():

#     # each instance of class will have a claim - purpose of object is to find evidence for given claim
#     def __init__(self, claim):
#         self.claim = claim

#     def search_claim(self):
#         search_results = search(self.claim, num_results=10, stop=10)
#         return search_results

# test_object = evidence_retrieval("the earth is flat")
# print(test_object.search_claim())

from bs4 import BeautifulSoup
import requests
import spacy

class evidence_retrieval():
    news_sites = ["https://www.bbc.co.uk/news", "https://www.theguardian.com/uk", "https://www.independent.co.uk/", "https://www.telegraph.co.uk/news/", "https://www.mirror.co.uk/news/", "https://www.express.co.uk/news", "https://www.dailymail.co.uk/news/index.html", "https://www.thesun.co.uk/news/", "https://www.thetimes.co.uk/"]
    def __init__(self, claim):
        self.claim = claim

    def breakdown_claim(self):
        nlp = spacy.load("en_core_web_sm") # doesn't like this
        doc = nlp(self.claim)
        return [token.text for token in doc if not token.is_stop and not token.is_punct]

    def search_claim(self):
        # something using beautifulsoup probably
        # for loop through each news site, crawling for news articles relating to the topic of the claim
        # go with the assumption there is a topic for a given claim - test on a pair of <claim, topic>
        return None
    
# object = evidence_retrieval("the earth is flat")
# print(object.breakdown_claim())