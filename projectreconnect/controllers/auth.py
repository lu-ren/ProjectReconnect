from flask import Blueprint, redirect, url_for, flash, current_app, session
from flask.ext.login import login_user, logout_user, current_user
from projectreconnect.auth import FacebookSignIn
from projectreconnect.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def oath_login():
    if not current_user.is_anonymous:
        #already logged in
        return redirect(url_for('home.home'))
    return FacebookSignIn().authorize()

@auth_bp.route('/logout')
def logout():
    if current_user.is_anonymous:
        return redirect(url_for('home.home'))
    logout_user()
    return redirect(url_for('home.home'))

@auth_bp.route('/callback')
def oauth_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('home.home'))
    oauth = FacebookSignIn()
    social_id, username, email = oauth.callback()
    if social_id is None:
        return redirect(url_for('home.home'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        session['allowed'] = True
        return redirect(url_for('home.create_account'))
    login_user(user)
    return redirect(url_for('home.home'))
