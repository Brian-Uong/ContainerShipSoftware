from flask import Blueprint, render_template, session, url_for
import load
auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    session['previous_url'] = url_for('home')
    return render_template("home.html")

@auth.route('/balance')
def balance():
    session['previous_url'] = url_for('auth.balance')
    grid = session.get('grid_data', {})
    filename = session.get('manifest_file', "Unknown File")
    return render_template("balancing.html", grid=grid, filename=filename)

@auth.route('/unload_load')
def unload_load():
    session['previous_url'] = url_for('auth.unload_load')
    grid = session.get('grid_data', {})
    filename = session.get('manifest_file', "Unknown File")
    return render_template('unload_load.html', grid=grid, filename=filename)

@auth.route('/file_upload')
def file_upload():
    session['previous_url'] = url_for('file_upload')
    return render_template("auth.file_upload.html")



