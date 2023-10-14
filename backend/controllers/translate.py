import mimetypes
import tempfile
from unittest import result
import certifi
from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import mail
from methods import translate, save_s3, download
from setup import ExtendedAPI, db, create_app
from models.file import File
import json

# ファイルを受け取って翻訳して返す機能のテスト
file_translation_bp = Blueprint('file_translation', __name__, url_prefix='/file')
class FileTranslation(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        file_array = []
        my_files = File.query.filter_by(user_id=user_id)
        for file in my_files:
            file_dict = {}
            file_dict["file_name"] = file.file_name
            file_dict["file_path"] = file.file_path
            file_array.append(file_dict)
        return jsonify(file_array)

    @jwt_required()    
    def post(self):
        # 翻訳
        input_data = request.files['file']
        # mimetype = input_data.content_type
        fp = tempfile.NamedTemporaryFile(suffix=".mp3")
        file_name = input_data.filename
        file_contents = input_data.read()
        fp.write(file_contents)
        translated_file = translate(fp)
        result_file_name = file_name.split('.')[0]+'_translated.mp3'
        save_s3(translated_file,result_file_name)
        result_file_path = "https://transpod.s3.ap-northeast-1.amazonaws.com/translated/"+result_file_name
        # DB登録処理
        user_id = get_jwt_identity()
        reslut_file = File(user_id=user_id, file_name=result_file_name,file_path=result_file_path)
        app = create_app()
        with app.app_context():
            db.session.add(reslut_file)
            db.session.commit()
        return 'done'

file_translation = ExtendedAPI(file_translation_bp)
file_translation.add_resource(FileTranslation, '')