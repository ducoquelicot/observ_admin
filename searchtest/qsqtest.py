from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

es = Elasticsearch()
q = Q("query_string",
        default_field = "body",
        query = "This OR cat +type : minutes +city : paloalto"
    )

s = Search(using=es, index="records").query(q)
total = s.count()
s = s[0:total]
response = s.execute()

for hit in response.hits.hits:
    print("ID: {} \nCity: {} \nType: {}\nBody: {} \n".format(hit['_id'], hit['_source']['city'], hit['_source']['type'], hit['_source']['body']))
