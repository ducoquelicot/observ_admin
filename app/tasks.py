from datetime import datetime
from app import db
from app.models import User, Record, Subscription
import ast
from app.search import query_index
from app.emails import send_results_email

def sub_job(expression, doctype, city, subid):
        # results, total = Record.search(expression, doctype, city)
        sub = Subscription.query.filter_by(id=subid).first()
        ids, total = query_index(expression, doctype, city)
        
        #TODO change == to >
        if total == sub.total:
                stored_results = ast.literal_eval(sub.output)
                new_ids = list(set(stored_results) ^ set(ids))
                when = [(1, 0), (2, 1), (3, 2)]

                for i in range(len(new_ids)):
                        when.append((new_ids[i], i))
                output = Record.query.filter(Record.id.in_(new_ids)).order_by(
                        db.case(when, value=Record.id))
                
                user = User.query.filter_by(id=sub.user_id).first()
                send_results_email(user, sub, output)

                sub.output = repr(ids)
                sub.total = total
        # return results, total
