from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from setup import create_app, db

import os
import sys
sys.path.append('../')

from models.user import User

login_bp = Blueprint('login', __name__, url_prefix='/login')
class LogIn(Resource):
    def post(self):
        req = request.json
        req_email = req["email"]
        req_password = req["password"]
        user = User.query.filter_by(email=req_email).first()
        if check_password_hash(user.password, req_password):
            access_token = create_access_token(identity = user.id)
            refresh_token = create_refresh_token(identity=user.id)
            user_id = user.id
            return jsonify(access_token=access_token, refresh_token=refresh_token, user_id=user_id)
        else:
            return 'login failed'

login = Api(login_bp)
login.add_resource(LogIn, '')