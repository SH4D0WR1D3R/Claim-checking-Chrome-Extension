# The application to run when wanting to run the fact checking process

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
import subprocess
import evidence_sentence_comparison

# Initialising as a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

global evidence
evidence = []
global retrieve_top_claims
top_claims = []

# DEFAULT URL
@app.route("/")
def default():
    return jsonify({''})

# POST REQUEST TO PROCESS HTML - puts together all aspects of the fact checking pipeline and returns results
@app.route("/process_html", methods=['POST'])
def process_html():
    # create an instance of the claim_detection class
    claim_detection_object = claim_detection.claim_detection()
    # get the html from the request
    data = request.get_json() # parses the incoming JSON request data from the HTTP POST request and returns it
    html = data.get('html') 

    # CLAIM DETECTION
    
    # set the pure html in the claim_detection object
    claim_detection_object.set_article_html(html)
    # move html to a file
    claim_detection_object.convert_to_file()
    # filter the pure html down to just the article contents
    title, article_content = claim_detection_object.filter_article_html()
    # rank each of the sentences in the article
    ranked_sentences = claim_detection_object.filter_sentences()
    # get sentences with scores over a defined threshold - means they are claim worthy/worth verifying
    top_sentences = claim_detection_object.find_top_sentences()

    # TRIGGER EVIDENCE RETRIEVAL SPIDER ON TOP 3 CLAIMS FOUND
    global top_claims
    top_claims = top_sentences    
    global evidence
    evidence = []
    sorted_top_claims = sorted(top_claims, key=lambda x: x['score'])
    sorted_top_claims = sorted_top_claims[:3]
    print("SORTED TOP CLAIMS: ", sorted_top_claims)

    # EVIDENCE RETRIEVAL
    for claim in sorted_top_claims:
        claim = claim['text']
        results = subprocess.Popen(['python', 'crawler.py', '--query', claim], stdout=subprocess.PIPE).communicate()[0]

    # example output
    # {'https://www.telegraph.co.uk/royal-family/2024/02/10/king-thanks-nation-messages-support/': {'version': '2', 'sentences': '\n\t\t\tLetter talks of his ‘lifelong admiration’ for all those who support cancer patients\n\t\tThe King has offered his “most heartfelt thanks” to the British public for their support after his cancer diagnosis, saying their kind thoughts are the “greatest comfort and encouragement”. In his first public comments acknowledging his illness, the King sent a message to the nation recognising the goodwill he has been shown since Buckingham Palace announced his diagnosis less than a week ago. Writing from Sandringham, Norfolk, where he is working from home and resting after his first bout of treatment, the King spoke of his “lifelong admiration” for all those who support cancer patients. It is “all the greater”, he said, now that he has experienced their care personally. The King is undergoing treatment for an unspecified cancer, and will be spending most of each week at Sandringham or Highgrove away from public engagements to protect his health. He is expected to return to London more or less weekly, in order to hold his audience with the Prime Minister and receive further treatment and medical advice. In his message to the nation, the King said: “I would like to express my most heartfelt thanks for the many messages of support and good wishes I have received in recent days. “As all those who have been affected by cancer will know, such kind thoughts are the greatest comfort and encouragement. “It is equally heartening to hear how sharing my own diagnosis has helped promote public understanding and shine a light on the work of all those organisations which support cancer patients and their families across the UK and wider world. “My lifelong admiration for their tireless care and dedication is all the greater as a result of my own personal experience. ”The NHS has reported a significant rise in people searching for symptoms of cancer since the King’s diagnosis, 51 per cent more than usual in the days following the announcement. The message was signed “Charles R”. This week, the King is not expected to be seen on any public engagements, although he may see the Prime Minister in person and will be conducting his usual official duties from his office. The Prince and Princess of Wales are spending half term with their three children as the Princess recuperates from abdominal surgery.  She will not resume her public duties until Easter at the earliest. The Prince returned to work for one day this week for an investiture and a charity fundraiser, having taken time off to be with his wife in hospital on most days of her two-week stay.  He will be back to his normal programme after the school holiday. The family is reported to be staying at Anmer Hall, its Norfolk home, from which William can visit his father privately. The Queen has said the King has been “very touched” by the messages he has received since his diagnosis was made public.  Before that, he had been treated for symptoms of an enlarged prostate, and was greeted by a crowd of well wishers when he left his London hospital. ', 'results': [{'text': '\n\t\t\tLetter talks of his ‘lifelong admiration’ for all those who support cancer patients\n\t\tThe King has offered his “most heartfelt thanks” to the British public for their support after his cancer diagnosis, saying their kind thoughts are the “greatest comfort and encouragement”.', 'index': 0, 'score': 0.2314195309}, {'text': 'In his first public comments acknowledging his illness, the King sent a message to the nation recognising the goodwill he has been shown since Buckingham Palace announced his diagnosis less than a week ago.', 'index': 1, 'score': 0.6381113492}, {'text': 'Writing from Sandringham, Norfolk, where he is working from home and resting after his first bout of treatment, the King spoke of his “lifelong admiration” for all those who support cancer patients.', 'index': 2, 'score': 0.3333529783}, {'text': 'It is “all the greater”, he said, now that he has experienced their care personally.', 'index': 3, 'score': 0.1400462987}, {'text': 'The King is undergoing treatment for an unspecified cancer, and will be spending most of each week at Sandringham or Highgrove away from public engagements to protect his health.', 'index': 4, 'score': 0.4195031786}, {'text': 'He is expected to return to London more or less weekly, in order to hold his audience with the Prime Minister and receive further treatment and medical advice.', 'index': 5, 'score': 0.4175275519}, {'text': 'In his message to the nation, the King said: “I would like to express my most heartfelt thanks for the many messages of support and good wishes I have received in recent days.', 'index': 6, 'score': 0.2461789344}, {'text': '“As all those who have been affected by cancer will know, such kind thoughts are the greatest comfort and encouragement.', 'index': 7, 'score': 0.0940491596}, {'text': '“It is equally heartening to hear how sharing my own diagnosis has helped promote public understanding and shine a light on the work of all those organisations which support cancer patients and their families across the UK and wider world.', 'index': 8, 'score': 0.1918835251}, {'text': '“My lifelong admiration for their tireless care and dedication is all the greater as a result of my own personal experience.', 'index': 9, 'score': 0.1032119112}, {'text': '”The NHS has reported a significant rise in people searching for symptoms of cancer since the King’s diagnosis, 51 per cent more than usual in the days following the announcement.', 'index': 10, 'score': 0.8397939446}, {'text': 'The message was signed “Charles R”.', 'index': 11, 'score': 0.4195631827}, {'text': 'This week, the King is not expected to be seen on any public engagements, although he may see the Prime Minister in person and will be conducting his usual official duties from his office.', 'index': 12, 'score': 0.2974393936}, {'text': 'The Prince and Princess of Wales are spending half term with their three children as the Princess recuperates from abdominal surgery.', 'index': 13, 'score': 0.5379508584}, {'text': 'She will not resume her public duties until Easter at the earliest.', 'index': 14, 'score': 0.2396286174}, {'text': 'The Prince returned to work for one day this week for an investiture and a charity fundraiser, having taken time off to be with his wife in hospital on most days of her two-week stay.', 'index': 15, 'score': 0.5067828262}, {'text': 'He will be back to his normal programme after the school holiday.', 'index': 16, 'score': 0.3247484554}, {'text': 'The family is reported to be staying at Anmer Hall, its Norfolk home, from which William can visit his father privately.', 'index': 17, 'score': 0.4793107459}, {'text': 'The Queen has said the King has been “very touched” by the messages he has received since his diagnosis was made public.', 'index': 18, 'score': 0.2444350242}, {'text': 'Before that, he had been treated for symptoms of an enlarged prostate, and was greeted by a crowd of well wishers when he left his London hospital.', 'index': 19, 'score': 0.3431097465}]}}
    # format: {<url>: {<version>: <int>, <sentences>: <str>, <results>: [{<text>: <str>, <index>: <int>, <score>: <float>}, ...]}}
    # print("\n\n\n\n END")
    # Format of results: b"The next line are links from evidence_retrieval: \r\n[<strings of urls>]
        results = parse_evidence(results)
        # need to call a function to extract claims from articles found
        evidence_judgements = []

        # ARTICLE JUDGEMENT
        for result in results:
            # filter down results to be useable in comparison
            result = result.replace("'", "")
            sentence_object = evidence_sentence_comparison.evidence_sentence_comparison(result, claim)
            judgements = sentence_object.run()
            evidence_judgements.append({result: judgements})
        evidence.append({claim: evidence_judgements})
    
    return evidence

# Method to return evidence from the global variable
@app.route("/retrieve_evidence", methods=['GET'])
def retrieve_evidence():
    print("EVIDENCE ", evidence)
    return evidence

# Method to return claims from the global variable
@app.route("/process_claim", methods=['POST'])
def process_claim():
    claim = request.get_json()
    claim_text = claim.get('claim')
    # print("CLAIM TEXT: ", claim_text)
    return claim_text

# Method to strip retrieved evidence of tags and string components
def parse_evidence(evidence):
    result = str(evidence).replace("b'[", "[")
    result = str(result).split("article")
    result = result[0]
    result = str(result).replace("]\\r\\n", "]")
    result = str(result).replace('b"', "")
    result = result.split("\\r\\n")
    result = result[1]
    result = result.replace("]", "")
    result = result.replace("[", "")
    result = result.split(",")
    return result

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
