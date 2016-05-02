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
    current_user.genomic_obj = genome
    db.session.commit()

def run_match(user):
    users = User.query.filter(User.uid != user.uid).all()
    params = []
    for u in users:
        modified = numpy.insert(u.genomic_obj, 0, u.uid)
        params.append(modified.tolist())
    allOthers = numpy.array(params)
    me = numpy.insert(user.genomic_obj, 0, user.uid)
    results = get_matches(allOthers, me, alleleFreq)
    return results

def get_match_results(results):
    matches = []
    for r in results:
        user = User.query.filter_by(uid=r[0].item()).first()
        lst = ['Name', user.full_name, 'Age', user.age, 'Email', user.email, 'PercentMatch', r[1]]
        i = iter(lst)
        matches.append(dict(zip(i,i)))
    return matches
