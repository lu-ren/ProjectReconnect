from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField
from wtforms import TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional
from wtforms.validators import Length, Email

class SignInForm(Form):
    email = TextField('Email address', validators=[
        Required('Please provide a valid email address')])
    password = PasswordField('Password Field', validators=[
        Required('Please provide a password')])
        

class SignUpForm(Form):
    name = TextField('Name', validators=[
        Required('Please provide a name'),
        Length(min=3, message=(u'Name is too short'))])

    email = TextField('Email address', validators=[
        Required('Please provide a valid email address'),
        Length(min=6, message=(u'Email address too short')),
        Email(message=(u'That\'s not a valid email address'))])

    password = PasswordField('Pick a secure password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match'),
        Length(min=6, message=(u'Please pick a longer password'))])

    confirm = PasswordField('Confirm password')
