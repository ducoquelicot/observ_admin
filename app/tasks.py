from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from .models import Record
import time

jobstores = {
    'default' : SQLAlchemyJobStore(url='sqlite:////home/fabienne/Desktop/Observ/observ.db', tablename='tasks')
}

def test(expression, city, doctype):
    results, total = Record.search(expression, doctype, city)
    print(results, total)
    for result in results:
        print(result)

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.add_job(test, 'interval', minutes=1, args=['police', 'paloalto', 'agenda'], id='1', name='test job')


# scheduler.add_job(test_job, 'interval', seconds=3)
scheduler.start()
print('Press CTRL+C to exit')

try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()