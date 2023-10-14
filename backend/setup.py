from flask import Flask, jsonify, make_response
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_restful.utils import http_status_message
from flask_jwt_extended import JWTManager, jwt_required
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from jwt import ExpiredSignatureError

# from flask_migrate import Migrate
import os
from datetime import datetime
from methods import mail
from config import LocalConfig

db = SQLAlchemy()
jwt = JWTManager()

class ExtendedAPI(Api):
    def handle_error(self, err):
        if isinstance(err, ExpiredSignatureError):
            return make_response(jsonify({'status': 'ACCESS_TOKEN_EXPIRED', 'message': 'token expired',}), 401)

def create_app():
    print('create_app')
    
    load_dotenv()
    app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')
    app.config.from_object(LocalConfig)

    # DB初期化
    db.init_app(app)
    # migrate = Migrate(app,db)

    # JWT初期化
    jwt.init_app(app)

    # メール初期化
    mail.init_app(app)

    return app

