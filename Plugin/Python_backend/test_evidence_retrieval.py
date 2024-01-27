import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scrapy.selector import Selector
import time
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class BBCSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['https://www.bbc.co.uk'] # something to add to

    # def __init__(self):

    def start_requests(self):
        search_term = 'Thousands stranded at New Year as Eurostar cancelled'
        search_url = f'https://duckduckgo.com/html/?q={search_term}&type=article'
        # search_url = f'https://www.bbc.co.uk/search?q={search_term}&type=article'
        # this type of querying doesn't work for the independent, for example
        request = scrapy.Request(url=search_url, callback=self.parse_search_results)
        # SHOULDN'T USE MY LOCAL TOKEN
        # request.cookies()
        yield request # set the cookies token somehow
        

    def parse_search_results(self, response):
        # response is the response of the request where this function is called
        # is a Response object?
        # article_links = response.css('a::attr(href)').extract()
        print("PARSE_SEARCH_RESULTS")
        soup = BeautifulSoup(response.body, 'html.parser')
        # need to extract non header and footer stuff
        print(soup.prettify())
        href_links = [a.get('href') for a in soup.find_all('a', href=True)]
        # some form of regex 
        print("HREF ", href_links)

        article_links = response.css('a::attr(href)').getall()


        # so this doesn't work. need to delve into different divs to find relevant links
        
        # currently its getting nothing for the first 2 things and only doing the parse article bit

        # once able to access these links, need to be able to go through those links?
        for link in href_links:
            try:
                yield scrapy.Request(url=link, callback=self.parse_article) # in theory this should go through found links and parse those articles
            except:
                pass

    def parse_article(self, response): # this isn't running
        print("Response", response)
        title = response.css('h1::text').get()
        # content = response.css('body::text').get()
        # content = response.css('p::text').getall() # CHANGE THIS
        # content is returning nothing
        yield {
            'title': title,
            # 'content': ' '.join(content),
            'url': response.url
        }

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output1.json'
})

process.crawl(BBCSpider)
process.start()