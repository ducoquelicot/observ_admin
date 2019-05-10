from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

es = Elasticsearch()
q = Q("bool",
      must = [
        Q("match",
          body = {
            "minimum_should_match" : 1,
            "query" : "cat",
            "operator" : "or"
            }
        )
    ]
)

s = Search(using=es, index="records").query(q)
total = s.count()
s = s[0:total]
response = s.execute()

print("Total hits: {}\n".format(total))

for hit in response.hits.hits:
    print("ID: {} \nCity: {} \nType: {}\nBody: {} \n".format(hit['_id'], hit['_source']['city'], hit['_source']['type'], hit['_source']['body']))