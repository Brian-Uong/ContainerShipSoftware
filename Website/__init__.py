from flask import Flask, request, redirect, url_for, session
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
        session['previous_url'] = url_for('home')
        return "Home Page"

    @app.route('/log', methods=['POST'])
    def log_message():
        log_message = request.form.get('logMessage')
        file_path = 'log.txt'

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + log_message + '\n')

        return redirect(session['previous_url'])
    
    # Crated 2 more log functions so user can stay on page where message was logged
    # @app.route('/logBalance', methods=['POST'])
    # def log_message_balance():
    #     log_message = request.form.get('logMessage')
    #     file_path = 'log.txt'

    #     with open(file_path, 'a') as files:
    #         files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + log_message + '\n')

    #     return redirect(url_for('auth.balance'))
    
    # @app.route('/logUnloadLoad', methods=['POST'])
    # def log_message_UnloadLoad():
    #     log_message = request.form.get('logMessage')
    #     file_path = 'log.txt'

    #     with open(file_path, 'a') as files:
    #         files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + log_message + '\n')

    #     return redirect(url_for('auth.unload_load'))
    
    @app.route('/signIn', methods=['POST'])
    def sign_in():
        sign_in = request.form.get('empName')
        file_path = 'log.txt'

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + sign_in + ' signs in.\n')

        return redirect(session['previous_url'])
    
    # # Created 2 more log functions for balancing and unload/load page
    # @app.route('/signInBalance', methods=['POST'])
    # def sign_in_Balance():
    #     sign_in = request.form.get('empName')
    #     file_path = 'log.txt'

    #     with open(file_path, 'a') as files:
    #         files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + sign_in + ' signs in.\n')

    #     return redirect(url_for('auth.balance'))
    
    # @app.route('/signInUnloadLoad', methods=['POST'])
    # def sign_in_UnloadLoad():
    #     sign_in = request.form.get('empName')
    #     file_path = 'log.txt'

    #     with open(file_path, 'a') as files:
    #         files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + sign_in + ' signs in.\n')

        return redirect(url_for('auth.unload_load'))
    
    @app.route('/homeRedirect', methods=['POST'])
    def homeRedirect():
        session['previous_url'] = url_for('home')
        return redirect(url_for('auth.home'))

    @app.route('/balanceRedirect', methods=['POST'])
    def balanceRedirect():
        return redirect(url_for('auth.balance'))
    
    @app.route('/unload_loadRedirect', methods=['POST'])
    def unload_loadRedirect():
        return redirect(url_for('auth.unload_load'))

    return app
