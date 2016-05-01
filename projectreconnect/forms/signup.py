from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, PasswordField, RadioField, \
    validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, NumberRange
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

    age = IntegerField('Age', validators=[
        Required('Please provide your age'),
        NumberRange(min=0, max=130, message=(u'Age must be between 0 and 130'))
    ])

    password = PasswordField('Pick a secure password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match'),
        Length(min=6, message=(u'Please pick a longer password'))])

    confirm = PasswordField('Confirm password')
