from flask import Blueprint, render_template, session, url_for, send_file
import load, os
auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    session['previous_url'] = url_for('home')
    return render_template("home.html")

@auth.route('/balance')
def balance():
    session['previous_url'] = url_for('auth.balance')
    grid = session.get('grid_data', {})
    print(grid)
    filename = session.get('manifest_file', "Unknown File")
    solution = session.get('solution_data', [])
    return render_template("balancing.html", grid=grid, filename=filename, solution=solution)

@auth.route('/unload_load')
def unload_load():
    session['previous_url'] = url_for('auth.unload_load')
    grid = session.get('grid_data', {})
    print(grid['1'][3])
    filename = session.get('manifest_file', "Unknown File")
    solution = session.get('solution_data', [])
    print(solution)
    return render_template('unload_load.html', grid=grid, filename=filename, solution=solution)

@auth.route('/file_upload')
def file_upload():
    session['previous_url'] = url_for('file_upload')
    return render_template("auth.file_upload.html")

@auth.route('/placeholder')
def placeholder():
    outbound_Folder = os.listdir("Website\outbound")
    if(outbound_Folder[0]):
        outbound_name = outbound_Folder[0]
        outbound_file_path = os.path.join(auth.root_path + '\outbound', outbound_name)
    return send_file(outbound_file_path, as_attachment=True)