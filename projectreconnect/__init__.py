from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import csv
import numpy
from .json_encoder import AlchemyEncoder

app = None
db = None
alleleFreq = []
with open('allele_data/allelefreq.csv', 'r') as f:
    reader = csv.reader(f)
    for elem in reader:
        alleleFreq.append(float(elem[0]))
alleleFreq = numpy.array(alleleFreq)

def init_app(config_filename):

    global db
    global app
    global Session

    app = Flask(__name__)
    app.config.from_object(config_filename)
    db = SQLAlchemy(app)

    import projectreconnect.models
    from projectreconnect.views import home_bp
    from projectreconnect.controllers import auth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
