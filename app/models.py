from app import db, login, observ
from app.search import query_index
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from time import time
import jwt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    organization = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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

class Record(SearchableMixin, db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    city = db.Column(db.String(64), index=True)
    doc_type = db.Column(db.String(64), index=True)
    date = db.Column(db.String(64))
    path = db.Column(db.String(200), index=True)


    def __repr__(self):
        return 'Record: {}\nCity: {}\nType: {}\nDate: {}\n\n'.format(self.name, self.city, self.doc_type, self.date)