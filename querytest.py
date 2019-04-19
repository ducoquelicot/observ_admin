from elasticsearch import Elasticsearch
es = Elasticsearch()

body={
  "query" : {
    "bool" : {
      "must" : [
        { "match" : {"type" : "agenda" } },
        { "bool" : {
          "minimum_should_match" : 1,
          "should" : [
            {"match" : {"city" : "paloalto" } },
            {"match" : {"city" : "redwoodcity" } }
            ]
          }
        },
        { "bool" : {
          "minimum_should_match": 1,
          "should" : [
            {"match" : {"body" : "Members" } },
            {"match" : {"body" : "Comment" } }
            ]
          }
        }
      ]
    }
  }
}

res = es.search(
    index="paloalto",
    body=body
)

for hit in res['hits']['hits']:
    print(hit['_score'], hit['_source'], hit['_id'])
