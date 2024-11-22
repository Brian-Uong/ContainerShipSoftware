from flask import Blueprint, render_template, session, url_for

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    session['previous_url'] = url_for('home')
    return render_template("home.html")

@auth.route('/balance')
def balance():
    session['previous_url'] = url_for('auth.balance')
    return render_template("balancing.html")

@auth.route('/unload_load')
def unload_load():
    session['previous_url'] = url_for('auth.unload_load')
    return render_template("unload_load.html")

# @auth.route('/signin')
# def signin():
#     return render_template("sign_in.html")

@auth.route('/file_upload')
def file_upload():
    session['previous_url'] = url_for('file_upload')
<<<<<<< HEAD
    return render_template("file_upload.html")
=======
    return render_template("auth.file_upload.html")
>>>>>>> 65bcb2e58ce20a486d2f44c742ac1538f3190204



