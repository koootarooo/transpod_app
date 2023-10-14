from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity,  jwt_required
from setup import jwt, create_app, ExtendedAPI

import os
import sys
sys.path.append('../')


refresh_bp = Blueprint('refresh', __name__, url_prefix='/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        print('refresh')
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify(access_token=access_token, refresh_token=refresh_token, user_id=user_id)

refresh = ExtendedAPI(refresh_bp)
refresh.add_resource(Refresh, '')