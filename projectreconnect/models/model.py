from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, \
             check_password_hash
from projectreconnect import db


class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    genomic_obj = db.Column(db.PickleType)
    pic_path = db.Column(db.String, default='none')
    description = db.Column(db.String)

    def __init__(self, full_name, age, email, password):
        self.full_name = full_name
        self.age = age
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)

    def __json__(self):
        return ['uid', 'full_name', 'phone_number']

    def __eq__(self, other):
        return (self.uid == other.uid)

    def __repr__(self):
        return "<User(uid=%s, full_name=%s, email=%s)> % \
            (self.uid, self.full_name, self.email)"
