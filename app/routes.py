from flask import render_template, flash, redirect, url_for, request
from app import observ, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, SearchForm, SubscriptionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Record, Subscription
from werkzeug.urls import url_parse
from app.emails import send_password_reset_email
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import time

@observ.route('/')
@observ.route('/index')
def index():
    return render_template('index.html')

@observ.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search_form = SearchForm()
    subscribe_form = SubscriptionForm()
    if search_form.validate():
        # return render_template('search.html', title='search', search_form=search_form, subscribe_form=subscribe_form)
        expression = search_form.q.data
        docs = search_form.doc_type.data
        cities = search_form.city.data
        doctype = ','.join(docs)
        city = ','.join(cities)
        results, total = Record.search(expression, doctype, city)

    if subscribe_form.validate_on_submit():
        subscription = Subscription(query=subscribe_form.query.data, city=subscribe_form.cities.data, doctype=subscribe_form.doctype.data, user=current_user)
        db.session.add(subscription)
        db.session.commit()
        flash('Subscription successfully added! You will receive an email shortly.')

        expression = subscribe_form.q.data
        docs = subscribe_form.doc_type.data
        cities = subscribe_form.city.data
        doctype = ','.join(docs)
        city = ','.join(cities)

        jobstores = {
        'default' : SQLAlchemyJobStore(url='sqlite:////home/fabienne/Desktop/Observ/observ.db', tablename='tasks')
        }

        def test(expression, doctype, city):
            results, total = Record.search(expression, doctype, city)
            return results, total

        scheduler = BackgroundScheduler(jobstores=jobstores)

        if subscribe_form.frequency.data == 'hourly':
            scheduler.add_job(test, 'interval', minutes=5, args=[expression, doctype, city], id=current_user.id, name=current_user.username)
        elif subscribe_form.frequency.data == 'daily':
            scheduler.add_job(test, 'interval', days=1, args=[expression, doctype, city], id=current_user.id, name=current_user.username)
        elif subscribe_form.frequency.data == 'weekly':
            scheduler.add_job(test, 'interval', weeks=1, args=[expression, doctype, city], id=current_user.id, name=current_user.username)
        
        results, total = test(expression, doctype,city)
        scheduler.start()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
        return render_template('search.html', title='search', results=results, total=total, search_form=search_form, subscribe_form=subscribe_form)
    return render_template('search.html', title='search', results=results, total=total, search_form=search_form, subscribe_form=subscribe_form)

@observ.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    search_form = SearchForm()
    subscribe_form = SubscriptionForm()
    if subscribe_form.validate_on_submit():
        subscription = Subscription(query=subscribe_form.query.data, city=subscribe_form.cities.data, doctype=subscribe_form.doctype.data, user=current_user)
        db.session.add(subscription)
        db.session.commit()
        flash('Subscription successfully added! You will receive an email shortly.')

        expression = subscribe_form.q.data
        docs = subscribe_form.doc_type.data
        cities = subscribe_form.city.data
        doctype = ','.join(docs)
        city = ','.join(cities)

        jobstores = {
        'default' : SQLAlchemyJobStore(url='sqlite:////home/fabienne/Desktop/Observ/observ.db', tablename='tasks')
        }

        def test(expression, doctype, city):
            results, total = Record.search(expression, doctype, city)
            return results, total

        scheduler = BackgroundScheduler(jobstores=jobstores)

        if subscribe_form.frequency.data == 'hourly':
            scheduler.add_job(test, 'interval', minutes=5, args=[expression, doctype, city], id=current_user.id, name=current_user.username)
        elif subscribe_form.frequency.data == 'daily':
            scheduler.add_job(test, 'interval', days=1, args=[expression, doctype, city], id=current_user.id, name=current_user.username)
        elif subscribe_form.frequency.data == 'weekly':
            scheduler.add_job(test, 'interval', weeks=1, args=[expression, doctype, city], id=current_user.id, name=current_user.username)
        
        results, total = test(expression, doctype,city)
        scheduler.start()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
        return render_template('search.html', title='search', results=results, total=total, search_form=search_form, subscribe_form=subscribe_form)
    return render_template('search.html', title='search', search_form=search_form, subscribe_form=subscribe_form)

@observ.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='login', form=form)

@observ.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))

@observ.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, organization=form.organization.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered.')
        return redirect(url_for('login'))
    return render_template('signup.html', title='sign up', form=form)

@observ.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='profile', user=user)

@observ.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.organization = form.organization.data
        db.session.commit()
        flash('Changes saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data  = current_user.username
        form.organization.data = current_user.organization
    return render_template('edit_profile.html', title='edit profile', form=form)

@observ.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='reset password', form=form)

@observ.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
