from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask import request

class LoginForm(FlaskForm):
    email = StringField('email address', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('sign in')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    organization = StringField('organization', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already in use.')

class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    organization = StringField('organization')
    submit = SubmitField('submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('request password reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('request password reset')

class SearchForm(FlaskForm):
    q = StringField('query', validators=[DataRequired()])
    doc_type = SelectMultipleField('document type', validators=[DataRequired()], choices=[('agenda', 'Agenda'), ('minutes', 'Minutes'), ('*', 'All')])
    city = SelectMultipleField('city', validators=[DataRequired()], choices=[('paloalto', 'Palo Alto'), ('redwoodcity', 'Redwood City'), ('*', 'All')])
    submit = SubmitField('search')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class SubscriptionForm(FlaskForm):
    query = StringField('query', validators=[DataRequired()])
    doctype = SelectMultipleField('document type', validators=[DataRequired()], choices=[('agenda', 'Agenda'), ('minutes', 'Minutes'), ('*', 'All')])
    cities = SelectMultipleField('city', validators=[DataRequired()], choices=[('paloalto', 'Palo Alto'), ('redwoodcity', 'Redwood City'), ('*', 'All')])
    frequency = RadioField('frequency', validators=[DataRequired()], choices=[('@hourly', 'Every hour'), ('@daily', 'Daily'), ('@weekly', 'Weekly')])
    submit = SubmitField('submit')