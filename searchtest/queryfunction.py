from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

def query_func():
    es = Elasticsearch()
    q = Q("query_string",
            default_field = "body",
            query = "This OR cat +type : minutes +city : paloalto"
        )

    s = Search(using=es, index="records").query(q)
    total = s.count()
    s = s[0:total]
    response = s.execute()

    output = "Total hits: {}\n\n".format(total)

    for hit in response.hits.hits:
        result = "ID: {} \nCity: {} \nType: {}\nBody: {}\n\n".format(hit['_id'], hit['_source']['city'], hit['_source']['type'], hit['_source']['body'])
        output += result
    
    return output

print(query_func())