import os

basedir = os.path.abspath(os.path.dirname(__file__)) #__file__ is the pathname of the file from which the module was loaded, if it was loaded from a file.


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1355882e53af1c504c2d2514779e1a2a' #>>>import secrets >>>secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') #add an email server for error handling
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['thomas.moellers@unisg.ch']

    COMPANY_NAME = "[COMPANY NAME STORED IN CONFIG]"
