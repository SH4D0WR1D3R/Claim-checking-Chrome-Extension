import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scrapy.selector import Selector
import time
from scrapy.crawler import CrawlerProcess

class BBCSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bbc.co.uk']
    # start_urls = ['https://www.cnn.com']

    # def __init__(self):

    def start_requests(self):
        search_term = 'global warming'
        search_url = f'https://www.bbc.co.uk/search?q={search_term}&type=article'
        yield scrapy.Request(url=search_url, callback=self.parse_search_results)
        

    def parse_search_results(self, response):
        article_links = response.css('a::attr(href)').extract() # css might need to change
        # so this doesn't work. need to delve into different divs to find relevant links
        
        # currently its getting nothing for the first 2 things and only doing the parse article bit
        for link in article_links:
            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        content = response.css('body').extract()
        # content is returning nothing
        yield {
            'title': title,
            'content': ' '.join(content),
            'url': response.url
        }

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json'
})

process.crawl(BBCSpider)
process.start()