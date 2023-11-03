import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.urandom(24)
    # メール設定
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('GMAIL_ADDRESS')
    MAIL_PASSWORD = os.environ.get('APP_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.environ.get('GMAIL_ADDRESS')

    # JWT設定
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JSON_AS_ASCII = False


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
                user=os.environ.get('POSTGRESQL_USER'),        
                password=os.environ.get('POSTGRESQL_PASSWORD'),  
                host="localhost",       
                port="5432",            
                dbname="transpod")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ACCESS_ALLOW_ORIGIN = 'http://localhost:8080'
    # 'postgresql:///' + os.path.join(basedir, 'app.db')

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
                user=os.environ.get('POSTGRESQL_USER'),        
                password=os.environ.get('POSTGRESQL_PASSWORD'),  
                host="localhost",       
                port="5432",            
                dbname="transpod")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ACCESS_ALLOW_ORIGIN = 'https://transpod-c78d3a6a1c42.herokuapp.com/'
    # 'postgresql:///' + os.path.join(basedir, 'app.db')