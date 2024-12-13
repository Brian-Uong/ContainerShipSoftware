from flask import Flask, Blueprint, render_template, session, url_for
import load, os
from load.manifest_read import parse
auth = Blueprint('auth', __name__)

app = Flask(__name__)

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
    folder_path = "Website\ManifestFolder"
    Manifest_Folder = os.listdir(folder_path)
    if (Manifest_Folder[0] == 'instructions.txt'):
        manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[1]))
        filename = Manifest_Folder[1]
    else:
        manifest_path = (os.path.join(app.root_path+'\ManifestFolder', Manifest_Folder[0]))
        filename = Manifest_Folder[0]
    ignore, grid_data = parse(manifest_path) #The ignore value being assigned is used in the astar search not the display grid.
    session['grid_data'] = {
        key: [{"weight": c.weight, "name": c.name} for c in containers]
        for key, containers in grid_data.items()
    }
    session['previous_url'] = url_for('auth.unload_load')
    grid = session.get('grid_data', {})
    filename = session.get('manifest_file', "Unknown File")
    return render_template('unload_load.html', grid=grid, filename=filename)

@auth.route('/file_upload')
def file_upload():
    session['previous_url'] = url_for('file_upload')
    return render_template("auth.file_upload.html")



