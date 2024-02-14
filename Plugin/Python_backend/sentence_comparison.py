from dotenv import load_dotenv
import os
import requests

class sentence_comparison:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ['CLAIMBUSTER_API_KEY']

    
    def similar_topic(self, sentence1, sentence2):
        endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/claim_similarity/simple_similarity/score/claim_a/{sentence1}/claim_b/{sentence2}"
        # TO DO: should do a check on sentences
        request_headers = {"x-api-key": self.api_key}
        api_response = requests.get(url=endpoint_url, headers=request_headers)
        if api_response.status_code == 200:
            # similarity_score = api_response.json()
            # print("SIMILARITY SCORE ", similarity_score)

            # return similarity_score
            results = api_response.json().get('results')[0] # list of dictionaries
            # print("RESULTS: ", results)
            score = results.get('similarity_score') # Score returning None
            # print("SCORE: ", score)
            if score > 0:
                return True
            return False

        else:
            print(f"Request failed with status code: {api_response.status_code}")
        
object = sentence_comparison()
print(object.similar_topic("The sky is blue", "The sky is green"))