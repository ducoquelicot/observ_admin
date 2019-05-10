from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

def query_func(expression, doctype, city):
    es = Elasticsearch()
    q = Q("query_string",
            default_field = "body",
            query = expression+ " +type : " +doctype+ " +city : " +city
        )

    s = Search(using=es, index="records").query(q)
    total = s.count()
    s = s[0:total]
    response = s.execute()

    ids = [hit['_id'] for hit in response.hits.hits]

    # output = "Total hits: {}\n\n".format(total)

    # for hit in response.hits.hits:
    #     result = "ID: {} \nCity: {} \nType: {}\nBody: {}\n\n".format(hit['_id'], hit['_source']['city'], hit['_source']['type'], hit['_source']['body'])
    #     output += result
    
    return ids, total

    # when = []
    # for i in range(len(ids)):
    #     when.append((ids[i], i))

    # return when

print(query_func("This OR cat","agenda","paloalto"))