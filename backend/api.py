import mimetypes
import tempfile
import certifi
from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource
from flask_mail import Message
from methods import mail
from methods import translate, save_s3, download
import json

# ファイルを受け取って翻訳して返す機能のテスト
file_translation_bp = Blueprint('file_translation', __name__, url_prefix='/api/post')
class FileTranslation(Resource):
    def get(self):
        msg = Message('Test Mail', recipients=['iikotaro3@yahoo.co.jp'])
        msg.body = "SECRET KEY was loaded successfully"
        mail.send(msg)
        return 'sent'

    def post(self):
        # 翻訳
        # input_data = request.files['file']
        # mimetype = input_data.content_type
        # fp = tempfile.NamedTemporaryFile(suffix=".mp3")
        # file_name = input_data.filename
        # file_contents = input_data.read()
        # fp.write(file_contents)
        # translated_text = translate(fp)
        # save_s3(fp,file_name)

        # downloaded_file = download()
        # メール
        # file_content_type = input_data.content_type
        # msg = Message('Test Mail', recipients=['iikotaro3@yahoo.co.jp'])
        # msg.body = "file was sent successfully."
        # mail.send(msg)
        return 'done'

file_translation = Api(file_translation_bp)
file_translation.add_resource(FileTranslation, '')