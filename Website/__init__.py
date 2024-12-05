import os
from flask import Flask, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from load.manifest_read import parse

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
        # print(request.files)
        file = request.files['manifest-input-balance']
        filename = secure_filename(file.filename)
        if filename == '': 
            session['previous_url'] = url_for('home')
            return redirect(url_for('home'))
        if file:
            manifest_path = (os.path.join(app.root_path+'\ManifestFolder', filename))
            file.save(manifest_path)

            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.
            except Exception as e:
                flash(f"ERRORRRRRR: {e}", "error")
                return redirect(url_for('home'))
            
            session['grid_data'] = {
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
        return redirect(url_for('auth.balance'))
    
    
    @app.route('/unload_loadRedirect', methods=['POST'])
    def unload_loadRedirect():
        #print(request.files)
        folder_path = "Website\ManifestFolder"
        Manifest_Folder = os.listdir(folder_path)
        file = request.files['manifest-input-unload-load']
        filename = secure_filename(file.filename)
        if len(Manifest_Folder) == 0: 
            manifest_path = (os.path.join(app.root_path+'\ManifestFolder', filename))
            file.save(manifest_path)

            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.

            except Exception as e:
                flash(f"ERRORRRRRR: {e}", "error")
                return redirect(url_for('home'))
            
            session['grid_data'] = {
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }

            return redirect(url_for('auth.unload_load'))
        else:
            manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[0]))
            try:
                ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.

            except Exception as e:
                flash(f"ERRORRRRRR: {e}", "error")
                return redirect(url_for('home'))
                
            session['grid_data'] = {
                key: [{"weight": c.weight, "name": c.name} for c in containers]
                for key, containers in grid_data.items()
                }
            return redirect(url_for('auth.unload_load'))


    @app.route('/completeCycle', methods=['POST'])
    def completeCycle():
        folder_path = "Website\ManifestFolder"
        Manifest_Folder = os.listdir(folder_path)
        for file in Manifest_Folder:
            file_path = os.path.join(folder_path, file)
            os.unlink(file_path)
        return redirect(url_for('home'))
    
    return app
