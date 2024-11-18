from flask import Flask, request, redirect, url_for
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key BEAM'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @app.route('/')
    def home():
        return "Home Page"

    @app.route('/log', methods=['POST'])
    def log_message():
        log_message = request.form.get('logMessage')
        file_path = 'log.txt'

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + log_message + '\n')

        return redirect(url_for('auth.unload_load'))
    @app.route('/signIn', methods=['POST'])
    def sign_in():
        sign_in = request.form.get('empName')
        file_path = 'log.txt'

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + sign_in + ' signs in.\n')

        return redirect(url_for('home'))
    
    @app.route('/balanceRedirect', methods=['POST'])
    def balanceRedirect():
        return redirect(url_for('auth.balance'))
    
    @app.route('/unload_loadRedirect', methods=['POST'])
    def unload_loadRedirect():
        return redirect(url_for('auth.unload_load'))

    return app
