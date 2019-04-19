from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

es = Elasticsearch()
q = Q("bool",
      must = [
        Q("match", type = "agenda"),
        Q("bool",
          minimum_should_match = 1,
          should = [
            Q("match", city = "paloalto"),
            Q("match", city = "redwoodcity")
            ]
        ),
        Q("bool",
          minimum_should_match = 1,
          should = [
            Q("match", body = "Members"),
            Q("match", body = "Comment")
            ]
        )
      ]
    )

s = Search(using=es, index="paloalto",).query(q)
total = s.count()
s = s[0:total]
response = s.execute()

print("Total hits: {}".format(total))

for hit in response.hits.hits:
    print("ID: {} \nCity: {} \nType: {}\nBody: {} \n".format(hit['_id'], hit['_source']['city'], hit['_source']['type'], hit['_source']['body']))