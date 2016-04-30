from flask import Blueprint, render_template, current_app, redirect, url_for, Markup, request, flash
from flask.ext.login import current_user, login_required
import json
from projectreconnect.forms.signup import SignInForm, SignUpForm
from projectreconnect.controllers.forms import create_account, check_account
from projectreconnect.models.model import User

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_anonymous:
        if request.method == 'POST':
            form = SignInForm(request.form)
            if form.validate():
                user = User.query.filter_by(email=form.email.data).first()
                if not user:
                    flash('Email does not exist')
                    return render_template('home.html', form=form)
                if not user.check_password(form.password.data):
                    flash('Invalid password')
                    return render_template('home.html', form=form)
                return redirect(url_for('home.dashboard', uid=user.uid))
        return render_template('home.html', form=SignInForm())
    else:
        return redirect(url_for('home.dashboard'), uid=current_user.uid)

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
                uid = create_account(form.name.data, form.email.data, form.password.data)
                return redirect(url_for('home.dashboard', uid=uid))
            else:
                return render_template('signup.html', form=form)
        return render_template('signup.html', form=SignUpForm())
    else:
        return redirect(url_for('home.home'))

@home_bp.route('/dashboard/<int:uid>')
@login_required
def dashboard(uid):
    return render_template('dashboard.html')
