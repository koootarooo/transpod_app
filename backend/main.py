from flask import Flask, render_template
from dotenv import load_dotenv
import os
from api import file_translation_bp
from methods import mail

load_dotenv()
app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')
app.register_blueprint(file_translation_bp)
# メール設定
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'iinemasuzawa@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('APP_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'iinemasuzawa@gmail.com'

mail.init_app(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, X-XSRF-TOKEN, Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run()