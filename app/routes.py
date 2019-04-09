from flask import render_template, flash, redirect, url_for, request
from app import observ, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@observ.route('/')
@observ.route('/index')
def index():
    return render_template('index.html')

@observ.route('/search')
@login_required
def search():
    return render_template('search.html', title='search')

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
    form = EditProfileForm()
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