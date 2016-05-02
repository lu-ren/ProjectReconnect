from flask import redirect, url_for, flash, current_app
import logging
from logging.handlers import RotatingFileHandler
from projectreconnect import init_app
import pdb

init_app('config.BaseConfig')
from projectreconnect import app

@app.before_first_request
def setup():
    from projectreconnect import db
    # db.drop_all() #for development purposes
    # db.create_all()
    # generate_sim_data()

def generate_sim_data():
    import csv
    import numpy
    import names
    from random import randint
    from projectreconnect.models import User
    from projectreconnect import db
    userslst = []
    namelst = []
    emaillst = []
    agelst = []
    genomelst = []
    with open('scripts/father0.txt') as f:
        reader = csv.reader(f)
        namelst.append('James Potter')
        genome = [int(s) for s in next(reader)[0]]
        # genome.insert(0,0)
        emaillst.append('jp3999@hogwarts.edu')
        agelst.append(58)
        genomelst.append(numpy.array(genome))
    pdb.set_trace()
    with open('scripts/100000_Simulated_Samples.txt') as f:
        reader = csv.reader(f)
        for x, elem in enumerate(reader):
            print(x)
            strlist = list(elem[0])
            numlist = [int(s) for s in strlist]
            # numlist.insert(0, 0)
            numlist = numpy.array(numlist)
            name = names.get_full_name()
            email = name.replace(" ", "") + "@email.com"
            namelst.append(name)
            emaillst.append(email)
            agelst.append(randint(20,100))
            genomelst.append(numpy.array(numlist))
    for x in range(len(namelst)):
        print(x)
        new_user = User(namelst[x], agelst[x], emaillst[x], 'password')
        new_user.genomic_obj = genomelst[x]
        db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    from flask.ext.login import LoginManager

    handler = RotatingFileHandler('general.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    login_manager = LoginManager(app)
    login_manager.login_view = 'home.home'

    @login_manager.user_loader
    def user_loader(user_id):
        from projectreconnect.models import User
        return User.query.get(int(user_id))

    app.run(debug=True)
