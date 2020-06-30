from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy
# import pandas as pd
import json

corpus = []

with open('data.json') as f:
    s = f.read()
    data = json.loads(s)
    
for summary in data['summaries']:
    corpus.append(summary['summary'])
    

vectorizer = TfidfVectorizer()
trsfm=vectorizer.fit_transform(corpus)
#pd.DataFrame(trsfm.toarray(),columns=vectorizer.get_feature_names(),index=['Document 0','Document 1'])
# cosine_similarity(trsfm, vectorizer.transform(['The Book in Three Sentences: The compound effect is the strategy of reaping huge rewards from small, seemingly insignificant until you measure it. Always take 100 percent responsibility for everything that happens to you']).toarray()).flatten()


def get_matched_books(query_strings, top_results_count):
    results_list = []
    #results_map = {'summary':"", 'id':0, 'query': ""}

    for query in query_strings:
        result = cosine_similarity(trsfm, vectorizer.transform([query]).toarray()).flatten()
        result_array = numpy.array(result)
        sort_index = numpy.argsort(result_array)

        for i in range(1,top_results_count+1) :
            index = int(sort_index[-1 * i])
            results_list.append({'summary':corpus[index], 'id':index, 'query': query})

    return results_list


app = Flask(__name__)

@app.route('/test_url', methods=['GET'])
def test_url():
    session = requests.Session()
    session.verify = False
    if(request.method == "GET"):
        search_key = request.args.get('q')
        search_result =  get_matched_books([search_key],3)

        relevant_books = []
        for i, item in enumerate(search_result):
            postJSON = json.dumps({'book_id':item.get('id')})
            endpoint = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding"
            response = requests.post(endpoint, postJSON).json()
            item['author'] = response['author']
            relevant_books.append(item)
        return jsonify({'books': relevant_books}), 201
    return False


if __name__ == "__main__":
    app.run(debug=True)