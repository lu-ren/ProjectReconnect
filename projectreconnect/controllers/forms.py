from flask import redirect, url_for
from projectreconnect.models import User
from projectreconnect import db
import pdb

def create_account(name, age, email, password):
    user = User(full_name=name, age=age, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
