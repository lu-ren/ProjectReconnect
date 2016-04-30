from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from .json_encoder import AlchemyEncoder

app = None
db = None

def init_app(config_filename):

    global db
    global app
    global Session

    app = Flask(__name__)
    app.config.from_object(config_filename)
    db = SQLAlchemy(app)

    import projectreconnect.models
    #import projectreconnect.auth
    from projectreconnect.views import home_bp
    from projectreconnect.controllers import auth_bp, forms_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(forms_bp, url_prefix='/form')
