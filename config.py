import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ABCDEFGHIJKLMOP'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    OPENWATER_MAIL_SUBJECT_PREFIX = '[Open Water] '
    OPENWATER_MAIL_SENDER = 'Open Water Admin <jeff@walkerjeff.com>'
    OPENWATER_ADMIN = 'jeff@walkerjeff.com'

    # S3_LOCATION = 'http://your-amazon-site.amazonaws.com/'
    S3_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    S3_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_UPLOAD_DIRECTORY = 'csvfiles'
    S3_BUCKET = os.environ.get('S3_BUCKET')

    UPLOADED_CSVFILES_DEST = os.path.join(basedir, 'uploads')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'open-water-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'open-water-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'open-water.sqlite')

class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}