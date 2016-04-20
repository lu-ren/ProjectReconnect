from flask import Blueprint
from .oath import OAuthSignIn

login = Blueprint('callback', __name__)

@auth_callback.route('/<provider>')
def callback(provider):
    pass