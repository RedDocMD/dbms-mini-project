from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        passwd = request.form['passwd']
        confirm_passwd = request.form['confirm-passwd']

        db = get_db()

        errors = []
        if not name:
            errors.append("Name is required")
        if not address:
            errors.append("Address is required")
        if not email:
            errors.append("Email is required")
        if not passwd:
            errors.append("Password is required")
        if passwd != confirm_passwd:
            errors.append("Passwords don't match")

        if not errors:
            return redirect(url_for('index'))

        for error in errors:
            flash(error)
    return render_template('signup.html')
