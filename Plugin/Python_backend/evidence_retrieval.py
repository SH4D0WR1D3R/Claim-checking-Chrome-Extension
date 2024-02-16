# Module to handle retrieving evidence based on a claim or set of claims

from bs4 import BeautifulSoup
import requests
import spacy
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from dotenv import load_dotenv
import os
from twisted.internet import reactor
import re

class evidence_retrieval_spider(scrapy.Spider):
    name = 'duckduckgo'
    allowed_domains = ['duckduckgo.com', 'bbc.co.uk', 'independent.co.uk', 'theguardian.com', 'telegraph.co.uk', 'thetimes.co.uk', 'dailymail.co.uk']
    start_urls = ['https://duckduckgo.com'] 
    # have a whitelist of domains to search through

    evidence_file = "evidence.txt"

    results = {}
    

    def __init__(self, search_term):
        self.evidence_and_articles_text = {}
        self.search_term = search_term
        load_dotenv()
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']
        # with open(self.html_file_name, "r", encoding="utf-8") as self.open_evidence_file:
        #     html_content = temp_html_file.read()
        # self.open_evidence_file.open(self.evidence_file, "w")


    # method to start the scraping
    def start_requests(self):
        # search_term = self.search_term
        search_url = f'https://duckduckgo.com/html/?q={self.search_term}&type=article'
        request = scrapy.Request(url=search_url, callback=self.parse_search_results)
        yield request

    # take the response and extract the html
    def parse_search_results(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # want to look for result_url class - duck duck go specific - holds full link
        # href_links = [a.get('href') for a in soup.find_all('a', href=True)]

        links = soup.find_all('a', class_="result__url")
        # print("\n\n", links, "\n\n") # testing
        # need to parse the list of tags to get the actual link
        new_links = self.parse_links(links)
        new_new_links = []

        print("OLD_LINKS ", new_links)
        # print(new_links)

        for link in new_links:
            
            for domain in self.allowed_domains:
                # if re.match(domain, link):
                if domain in link:
                    new_new_links.append(link)
        
                    

        # print("LINKS", new_new_links)
        # print("LINKS", new_links)
        print(new_new_links)


        # for link in href_links:
        #     try:
        #         yield scrapy.Request(url=link, callback=self.parse_article)
        #     except:
        #         pass

        # iterate through each link, call a function to parse the article
        for link in new_new_links:
            yield scrapy.Request(url=link, callback=self.parse_article)
            # try:
            #     # store link in dict - will be link:claims pairing
            #     yield scrapy.Request(url=link, callback=self.parse_article)
            # except:
            #     pass

    def get_link(self, link):
        return "https://" + str(link).split("</a>")[0].split(">")[-1].strip()

    def parse_links(self, links):
        # parse the list of links to get the actual link
        return [self.get_link(link) for link in links]
    
    # parse the article to get the text
    def parse_article(self, response):
        print("article")
        # need article tag
        link = response.url
        soup = BeautifulSoup(response.body, 'html.parser')
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            article_text = ''
            for paragraph in paragraphs:
                article_text += paragraph.text

            # now we have the text, need to pick claims out of it to compare
            # self.evidence_and_articles_text[link] = self.extract_claims(article_text)
            self.results[link] = self.extract_claims(article_text)
            # result = self.evidence_and_articles_text

        # print("DICT", self.evidence_and_articles_text)

    def extract_claims(self, article_text):
        article_text = article_text.replace(".", ". ")
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/score/text/sentences/{article_text}"
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            ranked_sentences = api_response.json()
            # print("SENTENCES ", ranked_sentences)
            return ranked_sentences
        else:
            print(f"Request failed with status code: {api_response.status_code}")
        

def run_spider(search_term):
    process = CrawlerProcess()
    process.crawl(evidence_retrieval_spider, search_term=search_term)
    process.start()
    return evidence_retrieval_spider.results

# runner = CrawlerRunner()
# d = runner.crawl(evidence_retrieval_spider, search_term="Thousands stranded at New Year as Eurostar cancelled")
# d.addBoth(lambda _: reactor.stop())
# reactor.run()