from elasticsearch import Elasticsearch
import os, glob

es = Elasticsearch()

txt_files = glob.glob(os.path.expanduser('~/Desktop/Python/Letters/*.txt'))

# for file in txt_files:
#     with open(file, 'r') as f:
#         text = f.read()
#     payload = {}
#     payload['city'] = "paloalto"
#     payload['doctype'] = "minutes"
#     payload["body"] = text
#     es.index(index="records", doc_type="_doc", body=payload)

with open(os.path.expanduser('~/Desktop/Python/Letters/letters_pdfs_2018_28_3.txt'), 'r') as f:
    text = f.readlines()
    date = text[0].rstrip()
    print(date)

