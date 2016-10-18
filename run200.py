from __future__ import division
from FeatureExtractor import get_collection, get_doc_term_matrix
import numpy as np
from os.path import join
from config import *
from Mallet import import_data, train_topics, doc_topic_matrix_from_file
from sklearn.cluster import KMeans, AgglomerativeClustering
from os.path import join
import sys
import pickle
from DocsetCreator import query_list
import itertools


def write_documents():
    texts = get_collection()
    i = 0
    for docID, text in texts.iteritems():
        file_path = join(DOCUMENTS_PATH, docID)
        with open(file_path, 'w') as f:
            f.write(text)

        i += 1
        sys.stdout.write("Documents Written to file: %d \r" %i)
        sys.stdout.flush()


def main():
    # import_data()
    # train_topics()
    matrix, docs = doc_topic_matrix_from_file()
    print "Storing docs to file!"
    with open('docs', 'w') as d:
        pickle.dump(docs, d)

    print "Clustering ..."
    model = KMeans(n_clusters=60)
    model = model.fit(matrix)
    labels = model.labels_
    print "Dumping the labels to file!"
    with open('labels', 'w') as f:
        pickle.dump(labels.tolist(), f)


def create_confusion_matrix():
    return


def load_from_file(filename):
    with open(filename, 'r') as l:
        return pickle.load(l)


def rel_docs(queries):
    with open(QRELS_PATH, 'r') as f:
        lines = f.readlines()

    docs_qID = {}
    for line in lines:
        split_line = line.split()
        qID = split_line[QID_INDEX]
        if qID in queries:
            docID = split_line[DOCID_INDEX]
            grade = int(split_line[REL_SCORE_INDEX])
            if grade == 1:
                docs_qID.setdefault(docID, []).append(qID)
    return docs_qID


if __name__ == '__main__':
    main()
    print "Loading labels ..."
    labels = load_from_file('labels')
    print "Loading docs ..."
    docs = load_from_file('docs')
    doc_map = {}
    for i, doc in enumerate(docs):
        doc_map[doc] = i

    queries = query_list()
    docs_qID = rel_docs(queries)
    combinations = list(itertools.combinations(docs_qID.keys(), 2))

    same_queries = [0, 0]
    diff_queries = [0, 0]
    for pair in combinations:
        first = pair[0]
        second = pair[1]
        first_cluster = labels[doc_map[first]]
        second_cluster = labels[doc_map[second]]
        if any(x in docs_qID[second] for x in docs_qID[first]):
            # same query
            if first_cluster == second_cluster:
                same_queries[0] += 1
            else:
                same_queries[1] += 1
        else:
            if first_cluster == second_cluster:
                diff_queries[0] += 1
            else:
                diff_queries[1] += 1

    print same_queries
    print diff_queries
    print len(combinations)
    print (same_queries[0] + diff_queries[1]) / len(combinations)