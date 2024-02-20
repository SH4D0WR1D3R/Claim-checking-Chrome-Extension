from dotenv import load_dotenv
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

class sentence_comparison:
    # def __init__(self, sentence1, sentence2):
    #     self.sentence1 = sentence1
    #     self.sentence2 = sentence2

    def sentences_agree(self, sentence1, sentence2):
        # format of return: {agreement: <agree, disagree, neutral>, cosine_similarity: <float>, sentiment_analysis_1: <positive, negative, neutral>, sentiment_analysis_2: <positive, negative, neutral>}

        # call cosine similarity function
        cosine_similarity_result = self.cosine_similarity(sentence1, sentence2)
        # if cosine similarity result is < 0.75 return false
        if cosine_similarity_result < 0.75:
            return {"agreement": "not related", "cosine_similarity": cosine_similarity_result, "sentiment_analysis_1": 0, "sentiment_analysis_2": 0}
        # else call sentiment analysis function on each sentence
        sentiment_analysis_1 = self.sentiment_analysis(sentence1)
        sentiment_analysis_2 = self.sentiment_analysis(sentence2)
        # if difference between sentiment analysis scores is < 0.1 return agree
        if abs(sentiment_analysis_1['score'] - sentiment_analysis_2['score']) < 0.1:
            return {"agreement": "agree", "cosine_similarity": cosine_similarity_result, "sentiment_analysis_1": sentiment_analysis_1, "sentiment_analysis_2": sentiment_analysis_2}
        # if difference between sentiment analysis scores is >= 0.5 return disagree
        elif abs(sentiment_analysis_1['score'] - sentiment_analysis_2['score']) >= 0.5:
            return {"agreement": "disagree", "cosine_similarity": cosine_similarity_result, "sentiment_analysis_1": sentiment_analysis_1, "sentiment_analysis_2": sentiment_analysis_2}
        # else return neutral
        else:
            return {"agreement": "neutral", "cosine_similarity": cosine_similarity_result, "sentiment_analysis_1": sentiment_analysis_1, "sentiment_analysis_2": sentiment_analysis_2}
    
    def cosine_similarity(self, sentence1, sentence2):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([sentence1, sentence2])
        similarity = cosine_similarity(vectors[0], vectors[1])
        return similarity[0][0]
    
    def sentiment_analysis(self, sentence):
        # define model path for sentiment analysis model
        model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        # define pipeline for sentiment analysis model
        sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
        # should return a dict of the form {'label': 'LABEL', 'score': SCORE}
        return sentiment_task(sentence)[0]


# class sentence_comparison:
#     def __init__(self):
#         load_dotenv()
#         self.api_key = os.environ['CLAIMBUSTER_API_KEY']

    
#     def similar_topic(self, sentence1, sentence2):
#         endpoint_url = f"https://idir.uta.edu/claimbuster/api/v2/claim_similarity/simple_similarity/score/claim_a/{sentence1}/claim_b/{sentence2}"
#         # TO DO: should do a check on sentences
#         request_headers = {"x-api-key": self.api_key}
#         api_response = requests.get(url=endpoint_url, headers=request_headers)
#         if api_response.status_code == 200:
#             # similarity_score = api_response.json()
#             # print("SIMILARITY SCORE ", similarity_score)

#             # return similarity_score
#             results = api_response.json().get('results')[0] # list of dictionaries
#             # print("RESULTS: ", results)
#             score = results.get('similarity_score') # Score returning None
#             # print("SCORE: ", score)
#             if score > 0:
#                 return True
#             return False

#         else:
#             print(f"Request failed with status code: {api_response.status_code}")

#     def cosine_similarity(self, sentence1, sentence2):
#         vectorizer = TfidfVectorizer()
#         vectors = vectorizer.fit_transform([sentence1, sentence2])
#         similarity = cosine_similarity(vectors[0], vectors[1])
#         return similarity[0][0]
    
#     def test_sentiment_analysis(self, sentence):
#         model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
#         sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
#         return sentiment_task(sentence) # s a list of a dictionary

        
object = sentence_comparison()
# print(object.similar_topic("The sky is blue", "The sky is green"))
print("COSINE ", object.cosine_similarity("The sky is blue", "The sky is not blue"))
print(object.sentiment_analysis("An HS1 spokesperson added on Saturday evening: \"We are doing everything possible to restore services but this is proving challenging and will take time.\""))
print(object.sentences_agree("The sky is blue", "The sky is not blue"))