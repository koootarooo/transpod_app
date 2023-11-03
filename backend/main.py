from flask import Flask, request, render_template, Response
from setup import create_app
import logging

app = create_app()

# blueprint
from controllers.translate import file_translation_bp
from controllers.signup import signup_bp
from controllers.login import login_bp
from controllers.refresh import refresh_bp
app.register_blueprint(file_translation_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(refresh_bp)

# ルート設定
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        print('preflight')
        return Response()

@app.after_request
def after_request(response):
    ORIGIN = app.config['ACCESS_ALLOW_ORIGIN']
    response.headers.add('Access-Control-Allow-Origin', f'{ORIGIN}')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, X-XSRF-TOKEN, Content-Type, Origin, Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run()