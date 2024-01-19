import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import options
from scrapy.selector import selector
import time

class CnnSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['www.cnn.com']
    start_urls = ['https://www.cnn.com']

    def __init__(self):
        chrome_options = options.Options()
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(executable_path=str('./chromedriver'), options=chrome_options)
        driver.get('https://www.bbc.co.uk/news')

        # begin search
        search_input = driver.find_element_by_id("footer-search-bar")
        search_input.send_keys("eurostar") # temporary topic search claim - maybe see if can replace with a claim
        search_btn = driver.find_element_by_xpath("(//button[contains(@class, 'Flex-sc-1)])[2]")
        search_btn.click()

        # record first page
        self.html = [driver.page_source]

        # start turning pages
        i=0 # number of sources to get
        while i<10: # they have 100 to get them from march 2021 to july 2020
            i += 1
            time.sleep(2)
            next_btn = driver.find_element_by_xpath("(//div[contains(@class, 'pagination-arrow)])[2]")
            next_btn.click()
            self.html.append(driver.page_source)

    def parse(self, response):
        for page in self.html:
            resp = selector(text=page)
            results = resp.xpath("//div[@class='cnn-search__result cnn-search__result--article']/div/h3/a")
            for result in results:
                title = result.xpath(".//text()").get()
                if ("Video" in title):
                    continue
                else:
                    link = result.xpath(".//@href").get()[13:] # cut off the domain
                    yield response.follow(url=link, callback=self.parse_article, meta={'title': title})

    def parse_article(self, response):
        title = response.request.meta['title']

        # don't care about author so not bothering with locating that

        # getting article body
        content = ' '.join(response.xpath("//section[@id='body-text']/div[@class='l-container']//text()").getall())
        if content is None:
            content = ' '.join(response.xpath("//div[@class='Article__content']//text()").getall())
            yield {
                "title": title,
                "byline": ' '.join(authors), # could be multiple authors
                "time": response.xpath("//p[@class='update-time']/text()").get(),
                "content": content
            }
