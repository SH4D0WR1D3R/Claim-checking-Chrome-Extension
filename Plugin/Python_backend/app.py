# file which is connected to frontend

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from bs4 import BeautifulStoneSoup
import claim_detection

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()
claim_detection_object = claim_detection.claim_detection()

# DEFAULT URL
@app.route("/")
def default():
    return jsonify({'message': 'Waiting for processes to run'})

@app.route("/process_html", methods=['POST'])
def process_html():
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
    claim_detection_object.find_top_sentences()

    # trigger rest of process here? evidence retrieval
    
    return jsonify({'message': 'HTML processed successfully'})

@app.route("/process_claim", methods=['POST'])
def process_claim():
    claim = request.get_json()
    claim_text = claim.get('claim')
    print("CLAIM TEXT: ", claim_text)
    # trigger the check of if it's claim worthy
    # maybe doesn't even need a check since the user wants it checked?


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
