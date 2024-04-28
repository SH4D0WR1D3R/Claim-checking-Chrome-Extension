# test file for evidence retrieval
import requests
from bs4 import BeautifulSoup

# need a white list of domains that can accept


# just need to do requests.get(<url>) to get html of web page

# get search_term passed in
# search_url = f'https://duckduckgo.com/html/?q={self.search_term}&type=article'

class evidence_retrieval:
    def __init__(self, search_term):
        self.search_term = search_term
        self.evidence_and_articles_text = {}

    def start_requests(self):
        # search_term = self.search_term
        search_url = f'https://duckduckgo.com/html/?q={self.search_term}&type=article'
        request = requests.get(search_url)
        return request.text

    # take the response and extract the html
    def parse_search_results(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # want to look for result_url class - duck duck go specific - holds full link
        # href_links = [a.get('href') for a in soup.find_all('a', href=True)]

        links = soup.find_all('a', class_="result__url")
        # print("\n\n", links, "\n\n") # testing
        # need to parse the list of tags to get the actual link
        new_links = self.parse_links(links)

        print(new_links)

        # iterate through each link, call a function to parse the article
        for link in new_links:
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
                
object = evidence_retrieval("Thousands stranded at New Year as Eurostar cancelled")
print(object.start_requests())