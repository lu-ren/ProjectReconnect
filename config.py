class BaseConfig(object):
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = 'postgresql://groupit:hx8889@localhost:5432/groupitdb'
        WTF_CSRF_ENABLED = True
        SECRET_KEY = 'mEpF4VR8TnxrEQ5b'
        OAUTH_CREDENTIALS = {'Facebook': {'id': '815578991921019',
                'secret': '17164f79145dafcaffbfbb86dd2f2128'}}

class TestConfig(BaseConfig):
        SQLALCHEMY_DATABASE_URI = 'postgresql://groupit:hx8889@localhost:5432/groupitdbtest'

class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testDB.db'

