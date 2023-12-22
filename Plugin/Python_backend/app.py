# file which is connected to frontend

from flask import Flask, request, jsonify

app = Flask(__name__)

# @app.route('/process_html', methods=['POST']) # specifies the URL endpoint and the accepted HTTP method
# def process_html():
#     if request.method == 'POST':
#         html_content = request.json.get('html')
#         # Process the received HTML content (e.g., using BeautifulSoup)
#         # Your processing logic here
        
#         # Return a response if needed
#         return jsonify({'message': 'HTML processed successfully'})

@app.route('/get_data')
def get_data():
    # Process your data here (e.g. fetching from database, processing etc)
    data = {'example': 'This is your processed data'}
    return jsonify(data)

@app.route("/")
def hi():
    return "Hi"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    # app.run(debug=True) # Run flask app