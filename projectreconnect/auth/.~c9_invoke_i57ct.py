from flask import Blueprint
from .oath import OAuthSignIn

logi = Blueprint('callback', __name__)

@auth_callback.route('/<provider>')
def callback(provider):
    pass