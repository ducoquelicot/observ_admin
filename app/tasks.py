from datetime import datetime
from app.models import Record

def test_job(expression, doctype, city):
        results, total = Record.search(expression, doctype, city)
        return results, total