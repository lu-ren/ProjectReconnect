from sqlalchemy.ext.associationproxy import association_proxy
from projectreconnect import db


class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.BigInteger, nullable=False)
    salt = db.Column(db.BigInteger, nullable=False)
    genomic_obj = db.Column(db.PickleType, nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.uid

    def is_anonymous(self):
        return False

    def __json__(self):
        return ['uid', 'full_name', 'phone_number']

    def __eq__(self, other):
        return (self.uid == other.uid)

    def __repr__(self):
        return "<User(uid=%s, full_name=%s, phone_number=%s)> % \
            (self.uid, self.full_name, self.phone_number)"
