from config import *


def get_documents():
    bm25_results = read_from_file(RESULTS_FILE_PATH)
    qrel_results = read_from_file(QRELS_PATH)
    union = {}
    for qID, docIDs in bm25_results.iteritems():
        union[qID] = list(set(docIDs + qrel_results[qID]))

    return union


def read_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    results = {}
    for line in lines:
        split_line = line.split()
        qID = split_line[QID_INDEX].strip()
        docID = split_line[DOCID_INDEX].strip()
        results.setdefault(qID, []).append(docID)

    return results


def query_list():
    query_doc = read_from_file(RESULTS_FILE_PATH)
    return query_doc.keys()


if __name__ == '__main__':
    query_doc = get_documents()
    print len(query_doc)
    print len(query_doc['61'])
