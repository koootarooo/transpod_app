from flask import Flask, jsonify, make_response
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_restful.utils import http_status_message
from flask_jwt_extended import JWTManager, jwt_required
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from jwt import ExpiredSignatureError
import logging

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
    app = Flask(__name__, static_folder='../dist/static', template_folder='../dist')
    app.config.from_object(LocalConfig)

    # ログ設定
    # gunicorn_err_logger = logging.getLogger("gunicorn.error")
    # gunicorn_err_logger.setLevel(logging.INFO)

    # gunicorn_access_logger = logging.getLogger("gunicorn.access")
    # gunicorn_access_logger.setLevel(logging.INFO)

    # sh = logging.StreamHandler()
    # sh.setLevel(logging.WARNING)

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # sh.setFormatter(formatter)

    # gunicorn_err_logger.addHandler(sh)
    # gunicorn_access_logger.addHandler(sh)

    # logging.basicConfig(level=logging.INFO, format='{asctime} [{levelname:.4}] {message}', style='{')
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("app.flask")
    logger.setLevel(logging.WARNING)

    # gunicorn
    # gunicorn_access_logger = logging.getLogger("gunicorn.access_log")
    # print(gunicorn_access_logger)
    # fh = logging.FileHandler("test.log")
    # gunicorn_access_logger.addHandler(fh)

    app.logger.info('create_app info')

    # DB初期化
    db.init_app(app)
    # migrate = Migrate(app,db)

    # JWT初期化
    jwt.init_app(app)

    # メール初期化
    mail.init_app(app)

    return app

