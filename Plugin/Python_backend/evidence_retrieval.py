# Module to handle retrieving evidence based on a claim or set of claims

from bs4 import BeautifulSoup
import requests
import spacy
import scrapy
from scrapy.crawler import CrawlerProcess

class evidence_retrieval_spider(scrapy.Spider):
    name = 'duckduckgo'
    allowed_domains = ['duckduckgo.com']
    start_urls = ['https://duckduckgo.com'] 
    # have a whitelist of domains to search through

    # method to start the scraping
    def start_requests(self):
        search_term = 'Thousands stranded at New Year as Eurostar cancelled'
        search_url = f'https://duckduckgo.com/html/?q={search_term}&type=article'
        request = scrapy.Request(url=search_url, callback=self.parse_search_results)
        yield request

    # take the response and extract the html
    def parse_search_results(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # want to look for result_url class - duck duck go specific - holds full link
        # href_links = [a.get('href') for a in soup.find_all('a', href=True)]

        links = soup.find_all('a', class_="result__url")
        print("\n\n", links, "\n\n")
        # need to parse the list of tags to get the actual link
        new_links = self.parse_links(links)

        print(new_links)

        # for link in href_links:
        #     try:
        #         yield scrapy.Request(url=link, callback=self.parse_article)
        #     except:
        #         pass

    def get_link(self, link):
        return str(link).split("</a>")[0].split(">")[-1].strip()

    def parse_links(self, links):
        # parse the list of links to get the actual link
        return [self.get_link(link) for link in links]

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output2.json'
})

process.crawl(evidence_retrieval_spider)
process.start()
    
# object = evidence_retrieval("the earth is flat")
# print(object.breakdown_claim())