# file which is connected to frontend

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

# DEFAULT URL
@app.route("/")
def default():
    return jsonify({'message': 'Waiting for processes to run'})

@app.route("/process_html", methods=['POST'])
def process_html():
    if request.method == 'POST':
        html_content = request.json.get('html')
        # insert code here to run claim detection?
        # probably need a global object to handle claim detection?
        # might be a way to make this code neater - class?
        print("Running process_html")
        print(html_content)
        return jsonify({'message': 'HTML processed successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    # app.run(debug=True) # Run flask app