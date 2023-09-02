from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource
from flask_mail import Message
from methods import mail
import json

# ファイルを受け取って翻訳して返す機能のテスト
file_translation_bp = Blueprint('file_translation', __name__, url_prefix='/api/post')
class FileTranslation(Resource):
    def get(self):
        msg = Message('Test Mail', recipients=['iikotaro3@yahoo.co.jp'])
        msg.body = "SECRET KEY was loaded successfully."
        mail.send(msg)
        return 'sent'

    def post(self):

        # postされたデータを読み込み
        input_data = request.files['file']

        return f'{input_data.filename}がアップロードされました'

file_translation = Api(file_translation_bp)
file_translation.add_resource(FileTranslation, '')