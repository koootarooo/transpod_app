from werkzeug.security import generate_password_hash
from flask import Blueprint, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from setup import create_app, db, ExtendedAPI

import os
import sys
sys.path.append('../')

from models.user import User

signup_bp = Blueprint('signup', __name__, url_prefix='/signup')
class SignUp(Resource):
    def post(self):
        print('posted')
        app = create_app()
        req = request.json
        req_email = req["email"]
        req_password = req["password"]
        user = User(email=req_email, password=generate_password_hash(req_password, method='pbkdf2'))
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        created_user = User.query.filter_by(email=req_email).first()
        user_id = created_user.id
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify(access_token=access_token, refresh_token=refresh_token, user_id=user_id)

signup = ExtendedAPI(signup_bp)
signup.add_resource(SignUp, '')
