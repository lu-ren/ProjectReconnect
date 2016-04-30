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
    db.drop_all() #for development purposes
    db.create_all()

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
