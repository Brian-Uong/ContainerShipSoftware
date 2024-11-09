from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/balance')
def balance():
    return render_template("balancing.html")

@auth.route('/unload_load')
def unload_load():
    return render_template("unload_load.html")

@auth.route('/signin')
def signin():
    return render_template("sign_in.html")

@auth.route('/file_upload')
def file_upload():
    return render_template("file_upload.html")



