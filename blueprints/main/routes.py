from flask import render_template, redirect, url_for
from flask_login import current_user
from . import main_bp


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('main/landing.html')
