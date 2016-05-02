class BaseConfig(object):
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = 'postgresql://projectreconnect@localhost:5432/projectreconnectdb'
        WTF_CSRF_ENABLED = True
        SECRET_KEY = 'mEpF4VR8TnxrEQ5b'
        UPLOAD_FOLDER = 'user_uploads/'
        ALLOWED_EXTENSIONS = set(['txt', 'csv'])

class TestConfig(BaseConfig):
        SQLALCHEMY_DATABASE_URI = 'postgresql://groupit:hx8889@localhost:5432/groupitdbtest'

class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testDB.db'

