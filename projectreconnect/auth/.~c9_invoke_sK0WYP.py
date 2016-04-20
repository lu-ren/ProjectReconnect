from flask import Blueprint
from .oath import OAuthSignIn

lo = Blueprint('callback', __name__)

@auth_callback.route('/<provider>')
def callback(provider):
    pass