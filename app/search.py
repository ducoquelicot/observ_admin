from elasticsearch_dsl import Search, Q
from app import observ, es, db
from app.models import Record

def query_index(expression, doctype, city):
    if not observ.config['ELASTICSEARCH_URL']:
        return [], 0
    q = Q("query_string",
                default_field = "body",
                query = "{} +doctype : {} +city : {}".format(expression, doctype, city)
        )

    s = Search(using=es, index="records").query(q)
    total = s.count()
    s = s[0:total]
    response = s.execute()

    # output = "Total hits: {}\n\n".format(total)

    # for hit in response.hits.hits:
    #     result = "ID: {} \nCity: {} \nType: {}\nBody: {}\n\n".format(hit['_id'], hit['_source']['city'], hit['_source']['type'], hit['_source']['body'])
    #     output += result

    # return output

    ids = [hit['_id'] for hit in response.hits.hits]

    return ids, total

def add_database(name, city, doctype, date, body):
    r = Record(
        name = name,
        city = city,
        doctype = doctype,
        date = date,
        body = body
    )
    db.session.add(r)
    db.session.commit()