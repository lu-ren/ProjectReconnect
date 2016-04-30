from flask import Blueprint, render_template, current_app, redirect, url_for, Markup
from flask.ext.login import current_user
import json

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_anonymous:
        return render_template('home.html')
    else:
        pass

@home_bp.route('/signup')
def signup():
    if current_user.is_anonymous:
        return render_template('signup.html')
    else:
        return redirect(url_for('home.home'))
