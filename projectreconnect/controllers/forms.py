from flask import redirect, url_for
from flask.ext.login import login_user
from projectreconnect.models import User
from projectreconnect import db
import pdb

def create_account(name, email, password):
    user = User(full_name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    #login_user(user, remember=True) For development purposes, disabled
    return user.uid
