import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'  #set configuration variables
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

#basedir = os.path.abspath(os.path.dirname(__file__)) 
# SQLALCHEMY_DATABASE_URI= 'sqlite:///'+ os.path.join(basedir, 'site.db')
# after importing-> URI; file on file system; set up as config; sqlite /// is realtive path from current file

