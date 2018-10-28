from flask import Blueprint, render_template, redirect, url_for

login = Blueprint('login', __name__, template_folder='templates')


@login.route('/')
def main():
    return redirect(url_for('login.login_page'))


@login.route('/login')
def login_page():
    return render_template('login.html')