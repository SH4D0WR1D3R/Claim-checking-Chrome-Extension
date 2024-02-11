# file which is connected to frontend

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from bs4 import BeautifulStoneSoup
import claim_detection
import evidence_retrieval as evidence_retrieval
import scrapy
from scrapy.crawler import CrawlerRunner, Crawler, CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor
from scrapy import signals
from scrapy.signalmanager import dispatcher
# from scrapy import log

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()


# DEFAULT URL
@app.route("/")
def default():
    return jsonify({'message': 'Waiting for processes to run'})

@app.route("/process_html", methods=['POST'])
def process_html():
    claim_detection_object = claim_detection.claim_detection()
    # get the html from the request
    data = request.get_json()
    html = data.get('html')

    # set the pure html in the claim_detection object
    claim_detection_object.set_article_html(html)

    # move html to a file
    claim_detection_object.convert_to_file()

    # filter the pure html down to just the article contents
    title, article_content = claim_detection_object.filter_article_html() # TO DO: WHY IS IT CUTTING OUT THE END OF THE ARTICLE? (list)

    # rank each of the sentences in the article
    ranked_sentences = claim_detection_object.filter_sentences()

    # get sentences with scores over a defined threshold - means they are claim worthy/worth verifying
    top_sentences = claim_detection_object.find_top_sentences()

    # trigger rest of process here? evidence retrieval

    # dispatcher might be useful?

    # have a variable here to store data from spider into
    # function to add to local variable
    # dispatcher.connect(function, signal=signals.item_scraped)

    # signals comes from "from scrapy import signals"

    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    runner = CrawlerRunner()
    d = runner.crawl(evidence_retrieval.evidence_retrieval_spider, search_term="Thousands stranded at New Year as Eurostar cancelled")
    # how can I extract the returned data from the spider?``
    d.addBoth(lambda _: reactor.stop())
    # add a callback to the spider to store the data in a variable
    d.addBoth(lambda _: print("RESULTS: ", results))
    reactor.run()
    # process = CrawlerProcess(Settings())
    # process.crawl(evidence_retrieval.evidence_retrieval_spider, search_term="Thousands stranded at New Year as Eurostar cancelled")
    # process.start()

    print("APP RESULTS: ", results)

    return jsonify({'message': 'HTML processed successfully'})


@app.route("/process_claim", methods=['POST'])
def process_claim():
    claim = request.get_json()
    claim_text = claim.get('claim')
    print("CLAIM TEXT: ", claim_text)
    # trigger the check of if it's claim worthy
    # maybe doesn't even need a check since the user wants it checked?
    return claim_text


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
