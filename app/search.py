from elasticsearch_dsl import Search, Q
from app import observ, es, db, models
import csv, os

def add_to_index(model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index="records", doc_type="_doc", id=model.id, body=payload)

def query_index(expression, doctype, city):
    if not observ.config['ELASTICSEARCH_URL']:
        return [], 0
    q = Q("query_string",
                default_field = "body",
                query = "({}) AND doctype:{} AND city:{}".format(expression, doctype, city)
        )

    s = Search(using=es, index="records").query(q)
    total = s.count()
    s = s[0:total]
    response = s.execute()

    ids = [hit['_id'] for hit in response.hits.hits]

    return ids, total