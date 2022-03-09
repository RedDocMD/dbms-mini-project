from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
import functools


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['passwd']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM User WHERE emailAddress = ?', (email,)).fetchone()
        if user is None:
            error = "Username doesn't exist"
        elif passwd != user['passwd']:
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['userId'] = user['userId']
            return redirect(url_for('index'))

        flash(error)
    return render_template('login.html')


@bp.before_app_first_request
def load_logged_in_user():
    user_id = session.get('userId')
    if user_id is None:
        g.user = None
    else:
        g.user - get_db().execute('SELECT * FROM User WHERE id= ?', (user_id, )).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


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
            try:
                db.execute(
                    "INSERT INTO User (fullName, emailAddress, passwd, userType) VALUES (?, ?, ?, ?)",
                    (name, email, passwd, "USR"),
                )
                userId = db.execute(
                    f'SELECT userId FROM User WHERE emailAddress = ?', (email,)).fetchone()[0]
                oldMaxAddressId = db.execute(
                    "SELECT MAX(addressId) FROM UserAddress").fetchone()[0]
                if oldMaxAddressId is None:
                    oldMaxAddressId = 0
                db.execute(
                    "INSERT INTO UserAddress (userId, addressId, addressName) VALUES (?, ?, ?)",
                    (userId, oldMaxAddressId + 1, address),
                )
                db.commit()
            except db.IntegrityError:
                errors.append(f"{email} is already registered")
            else:
                return redirect(url_for('index'))

        for error in errors:
            flash(error)
    return render_template('signup.html')
