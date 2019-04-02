from flask import render_template
from app import observ

@observ.route('/')
@observ.route('/index')
def index():
    return render_template('index.html')

@observ.route('/search')
def search():
    return render_template('search.html', title='search')