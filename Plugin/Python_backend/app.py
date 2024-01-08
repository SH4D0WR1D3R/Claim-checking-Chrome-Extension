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
# this method needs to get the information from side_panel.js - unsure how
def process_html():
    # PUT instead of POST
    # POST is used to create data
    # PUT is used to update data
    data = request.get_json()
    html = data.get('html')

    claim_detection_object.set_article_html(html)

    # move html to a file
    claim_detection_object.convert_to_file()

    # filter html in file and store in another file?
    title, article_content = claim_detection_object.filter_article_html() # WHY IS IT CUTTING OUT THE END OF THE ARTICLE? (list)
    # print("ARTICLE : ", article_content)

    # now have sentences of the article - article_content
    # do i get the rankings for sentences here as well?
    ranked_sentences = claim_detection_object.filter_sentences()
    # print(ranked_sentences)

    # print("Title: ", title)
    # print("Article Content: ", article_content)

    # trigger rest of process here? evidence retrieval

    claim_detection_object.find_top_sentences()
    
    return jsonify({'message': 'HTML processed successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    # app.run(debug=True) # Run flask app