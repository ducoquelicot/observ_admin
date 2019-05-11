from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'observ.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('mail_server')
    MAIL_PORT = os.environ.get('mail_port')
    MAIL_USE_TLS = os.environ.get('use_tls')
    MAIL_USERNAME = os.environ.get('mail_username')
    MAIL_PASSWORD = os.environ.get('dev_pass')
    ADMINS = ['fmeijer@stanford.edu']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {'default' : SQLAlchemyJobStore(url = SQLALCHEMY_DATABASE_URI)}
    SCHEDULER_EXECUTORS = {'default' : {'type': 'threadpool', 'max_workers' : 20}}
    SCHEDULER_JOB_DEFAULTS = {'coalesce' : False, 'max_instances' : 3}
    JOBS = [
        {
            'id' : 'test_job',
            'func' : 'advanced:test_job',
            'trigger:' : 'interval',
            'seconds' : 3
        }
    ]
