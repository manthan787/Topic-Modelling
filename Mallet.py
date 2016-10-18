import subprocess
from config import *
from scipy.sparse import coo_matrix
import sys
import numpy as np


def import_data():
    args = [MALLET_PATH, 'import-dir', '--input', DOCUMENTS_PATH, '--output', MALLET_COLLECTION_PATH,
            '--keep-sequence', '--remove-stopwords']
    subprocess.call(args)


def train_topics():
    print "Training topics ..."
    args = [MALLET_PATH, 'train-topics', '--input', MALLET_COLLECTION_PATH, '--output-doc-topics',
            MALLET_DOC_TOPICS_PATH, '--output-topic-keys', MALLET_TOPIC_KEYS_PATH, '--output-state',
            MALLET_OUTPUT_STATE_PATH, '--num-topics', str(NUM_TOPICS), '--num-threads', str(8)]

    subprocess.call(args)


def doc_topic_matrix_from_file():
    with open(MALLET_DOC_TOPICS_PATH, 'r') as f:
        lines = f.readlines()
    docs = []
    rows = []
    columns = []
    data = []
    for k, line in enumerate(lines[1:]):
        split_line = line.split()
        ID = int(split_line[0])
        docID = split_line[1].split('/')[-1].strip()
        docs.append(docID)
        for i in range(0, len(split_line[2:72]), 2):
            rows.append(ID)
            columns.append(split_line[2+i])
            data.append(float(split_line[2+i+1]))

        sys.stdout.write("Progress: %d \r" %k)
        sys.stdout.flush()

    print "Building the matrix!"
    rows = np.array(rows)
    columns = np.array(columns)
    data = np.array(data)
    matrix = coo_matrix((data, (rows, columns)), shape=((len(lines) - 1), 200))
    return matrix, docs