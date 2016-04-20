from flask import Blueprint, render_template, current_app, redirect, url_for, Markup
from flask.ext.login import current_user
from projectreconnect.models import Organization
import json

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_anonymous:
        return render_template('testhome.html')
    else:
        pass

@home_bp.route('/create_account')
def create_account():
    organizations = Organization.query.with_entities(Organization.name).all()
    lst = []
    for o in organizations:
        lst.append(o[0])
    lst.sort()
    return render_template('accountcreation.html', 
            formControllerUrl=url_for('form.create_account'), organizations=lst)
