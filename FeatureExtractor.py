import sys
from elasticsearch import Elasticsearch
from config import *
from sklearn.feature_extraction.text import CountVectorizer


es = Elasticsearch(timeout=1000)


def get_corpus(docs):
    """
    docs: List containing all the document IDs
    :return: a list containing text from each one of the IDs in docs
    """
    doc_map = {}
    texts = []
    for i, doc in enumerate(docs):
        doc_map[i] = doc
        search_body = SEARCH_BODY.format(id = doc)
        res = es.search(index=INDEX, doc_type=TYPE, body=search_body)
        hits = res['hits']['hits'][0]
        text = hits['fields']['text'][0]
        texts.append(text)

    return texts, doc_map


def get_collection():
    texts = {}
    page = es.search(index = INDEX, doc_type = TYPE, scroll = '2m', search_type = 'scan', size = 10000)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    # Start scrolling
    while (scroll_size > 0):
        print "Scrolling..."
        page = es.scroll(scroll_id = sid, scroll = '2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        hits = page['hits']['hits']
        for hit in hits:
            text = hit['_source']['text']
            if len(text) > 0:
                texts[hit['_id']] = text
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        print "scroll size: " + str(scroll_size)
    print "Total Documents: %s" %(len(texts))
    return texts


def get_doc_term_matrix(texts):
    print "Creating the doc term matrix!"
    vectorizer = CountVectorizer(stop_words='english', max_df=2.0, min_df=0.95, max_features=10000)
    matrix = vectorizer.fit_transform(texts)
    return matrix, vectorizer


if __name__ == '__main__':
    texts, map = get_collection()
    print len(texts)