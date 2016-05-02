from flask import redirect, url_for
from flask.ext.login import current_user
import numpy
from projectreconnect.models import User
from projectreconnect.core import get_matches
from projectreconnect import db, alleleFreq
import pdb

def create_account(name, age, email, password):
    user = User(full_name=name, age=age, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def update_user_genome(genome):
    current_user.genome_obj = genome
    db.session.commit()

def run_match(user):
    users = User.query.all()
    params = []
    for u in users:
        modified = numpy.insert(u.genome_obj, 0, u.uid)
        params.append(modified)
    allOthers = numpy.array(params)
    me = numpy.insert(user.genome_obj, 0, user.uid)
    results = get_matches(allOthers, me, alleleFreq)
    return results
