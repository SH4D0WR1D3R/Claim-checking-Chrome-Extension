
// Ideal format of data being received
// {claim1: 
// {evidence1: 
// {sentence1: 
// {agreement: <pos, neg, neut>, 
// cosine_similarity:<value>, 
// "sentiment_analysis_1": {"label":"negative","score":0.5319572687149048},
// "sentiment_analysis_2":{"label":"negative","score":0.8450345993041992}
// }
// }, evidence2: ...
// }, claim2...
// }


// actual format
// [{claim1: [{evidence1: [{sentence1: {agreement: <pos, neg, neut>, 
// cosine_similarity:<value>, 
// "sentiment_analysis_1": {"label":"negative","score":0.5319572687149048},
// "sentiment_analysis_2":{"label":"negative","score":0.8450345993041992}
// }}]}]}
// {claim2...}]

const testData = [{"claim1": [{"evidence1": [{"sentence1": {"agreement": "pos", "cosine_similarity": 0.5, "sentiment_analysis_1": {"label": "negative", "score": 0.5319572687149048}, "sentiment_analysis_2": {"label": "negative", "score": 0.8450345993041992}}}]}]}]
