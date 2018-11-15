from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.blueprints.login.forms import PassForm
from app.blueprints.login.login_required import login_required
from config.settings import DevelopmentConfig


login = Blueprint('login', __name__, template_folder='templates')


@login.route('/')
def main():
    if 'password' in session and session['password'] == DevelopmentConfig.PASSWORD:
        return redirect(url_for('library.index'))
    else:
        return redirect(url_for('login.login_page'))


@login.route('/login', methods=['POST', 'GET'])
def login_page():
    form = PassForm()
    if form.validate_on_submit():
        if form.password.data == DevelopmentConfig.PASSWORD:
            session['password'] = form.password.data
            flash('you are login!', 'success')
            return redirect(url_for('library.index'))
        else:
            flash('incorrect password', 'danger')
            return redirect(url_for('login.login_page'))
    return render_template('login.html', form=form)


@login.route('/logout')
@login_required()
def log_out():
    session.clear()
    return redirect(url_for('login.login_page'))
