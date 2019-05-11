from datetime import datetime

def test_job():
    with open('/tmp/flask_scheduler_test.txt', 'a') as log:
        log.write("{}\n".format(datetime.now()))
