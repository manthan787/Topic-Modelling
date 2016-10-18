from DocsetCreator import get_documents
from FeatureExtractor import get_corpus, get_doc_term_matrix
import lda
import numpy as np
from os.path import join
from config import *


query_doc = get_documents()
for qID, _ in query_doc.iteritems():
    texts, doc_map = get_corpus(query_doc[qID])
    mat, vec = get_doc_term_matrix(texts)
    vocab = vec.get_feature_names()
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(mat)
    n_top_words = 20
    topic_word = model.topic_word_
    doc_topic = model.doc_topic_
    string = ''
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        string += 'Topic {}: {}\n'.format(i, ' '.join(topic_words))

    for i in range(len(texts)):
        string += "{} (top topics: {})\n".format(doc_map[i], doc_topic[i].argsort()[::-1][:10])

    string += "\n"
    path = join(RESULTS_PATH, qID)
    with open(path, 'w') as f:
        f.write(string)