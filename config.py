import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'observ.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('DEV_PASS')
    ADMINS = ['fmeijer@stanford.edu']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {'default' : SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI, tablename='tasks')}
    # SCHEDULER_EXECUTORS = {'default' : {'type': 'threadpool', 'max_workers' : 20}}
    # SCHEDULER_JOB_DEFAULTS = {'coalesce' : False, 'max_instances' : 3}