from flask import redirect, url_for
from flask.ext.login import current_user
from projectreconnect.models import User
from projectreconnect import db
import pdb

def create_account(name, age, email, password):
    user = User(full_name=name, age=age, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def update_user_genome(genome):
    current_user.genome_obj = genome
    db.session.commit()
