from app import db, login, observ
from app.search import query_index, add_to_index
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from time import time
from datetime import datetime
import jwt, os, csv

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    organization = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            observ.config['SECRET_KEY'], algorithm='HS256').decode('utf-8'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, observ.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, doctype, city):
        ids, total = query_index(expression, doctype, city)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def add_database(cls):
        with open('pa_ag_2018.csv', 'r') as database:
            reader = csv.reader(database)
            database.readline()
            for row in reader:
                r = cls(
                    name = row[0],
                    city = row[1],
                    doctype = row[2],
                    date = row[3],
                    body = row[4]
                )
                db.session.add(r)
                db.session.commit()

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(obj)

class Record(SearchableMixin, db.Model):
    __tablename__ = 'records'
    __searchable__ = ['name', 'city', 'doctype', 'body']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    city = db.Column(db.String(64), index=True)
    doctype = db.Column(db.String(64), index=True)
    date = db.Column(db.String(64))
    body = db.Column(db.String(200), index=True)


    def __repr__(self):
        return 'Record: {} City: {} Type: {} Date: {}'.format(self.name, self.city, self.doctype, self.date)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q = db.Column(db.String(200), index=True)
    city = db.Column(db.Text, index=True)
    doctype = db.Column(db.String(64), index=True)
    frequency = db.Column(db.String(30), index=True)
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    output = db.Column(db.Text, index=True)
    total = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__ (self):
        return 'Subscription: {} City: {} Type: {} Frequency: {}'.format(self.q, self.city, self.doctype, self.frequency)