import os
from flask import Flask, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import datetime

def create_app():

    UPLOAD_FOLDER = '/'

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
    
    @app.route('/signIn', methods=['POST'])
    def sign_in():
        sign_in = request.form.get('empName')
        file_path = 'log.txt'

        with open(file_path, 'a') as files:
            files.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + sign_in + ' signs in.\n')

        return redirect(session['previous_url'])
    
    @app.route('/homeRedirect', methods=['POST'])
    def homeRedirect():    
        session['previous_url'] = url_for('home')
        return redirect(url_for('auth.home'))

    #These both take a file from their respective buttons on the home page and upload it to the ManifestFolder file. If there is no file selected it will keep them on the hope page.
    @app.route('/balanceRedirect', methods=['GET','POST'])
    def balanceRedirect():
        print(request.files)
        file = request.files['manifest-input-balance']
        filename = secure_filename(file.filename)
        if filename == '': 
            session['previous_url'] = url_for('home')
            return redirect(url_for('home'))
        if file:
            file.save(os.path.join(app.root_path+'\ManifestFolder', filename))
        return redirect(url_for('auth.balance'))
    
    
    @app.route('/unload_loadRedirect', methods=['POST'])
    def unload_loadRedirect():
        print(request.files)
        file = request.files['manifest-input-unload-load']
        filename = secure_filename(file.filename)
        if filename == '':
            session['previous_url'] = url_for('home')
            return redirect(url_for('home'))
        if file:
            file.save(os.path.join(app.root_path+'\ManifestFolder', filename))
        return redirect(url_for('auth.unload_load'))

    return app
