from flask import Blueprint, request, session, redirect, url_for
from projectreconnect.models import User
import pdb

forms_bp = Blueprint('form', __name__)

@forms_bp.route('/create_account', methods=['POST'])
def create_account():
    if 'allowed' in session:
        if session['allowed']:
            full_name = request.form['Name']
            school = request.form['School']
            subjects = request.form['Subjects']
    return redirect(url_for('home.home'))
