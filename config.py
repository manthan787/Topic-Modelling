RESULTS_FILE_PATH = '/Users/admin/Documents/CS6200/HW1/Query/Results/bm25_results'
QRELS_PATH = '/Users/admin/Documents/CS6200/AP_DATA/qrels.adhoc.51-100.AP89.txt'
RESULTS_PATH = '/Users/admin/Documents/CS6200/HW8/Results'
DOCUMENTS_PATH = '/Users/admin/Documents/CS6200/HW8/Documents'
MALLET_PATH = '/Users/admin/Downloads/mallet-2.0.7/bin/mallet'
MALLET_COLLECTION_PATH = '/Users/admin/Documents/CS6200/HW8/Mallet/docs.mallet'
MALLET_DOC_TOPICS_PATH = '/Users/admin/Documents/CS6200/HW8/Mallet/doc_topics'
MALLET_TOPIC_KEYS_PATH = '/Users/admin/Documents/CS6200/HW8/Mallet/topic_keys'
MALLET_OUTPUT_STATE_PATH = '/Users/admin/Documents/CS6200/HW8/Mallet/output_state.gz'
NUM_TOPICS = 200
QID_INDEX = 0
DOCID_INDEX = 2
REL_SCORE_INDEX = 3
INDEX = 'ap_dataset'
TYPE  = 'document'

SEARCH_BODY = """
{{
  "query": {{
    "match": {{
      "_id": "{id}"
    }}
  }},
  "fields":["text"]
}}
"""
