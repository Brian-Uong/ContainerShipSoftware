from flask import Blueprint, render_template, session, url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
    session['previous_url'] = url_for('home')
    return render_template("home.html")