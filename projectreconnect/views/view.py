from flask import Blueprint, render_template, current_app, redirect, url_for, Markup, request
from flask.ext.login import current_user
import json
from projectreconnect.forms.signup import SignUpForm
from projectreconnect.controllers.forms import create_account

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_anonymous:
        return render_template('home.html')
    else:
        pass

@home_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.form)
            if form.validate():
                email_exist = User.query.filter_by(email=form.email.data).first()
                if email_exist:
                    form.email.errors.append('Email already taken')
                    return render_template('signup.html', form=form)
                create_account(form.name.data, form.email.data, form.password.data)
                #stub, need to create dashboard
                return redirect(url_for('home.home'))
            else:
                return render_template('signup.html', form=form)
        return render_template('signup.html', form=SignUpForm())
    else:
        return redirect(url_for('home.home'))
