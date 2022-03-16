from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
import functools
import bcrypt


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
        elif not bcrypt.checkpw(passwd.encode('utf8'), user['passwd']):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['userId'] = user['userId']
            fullName = user['fullName']
            nameParts = fullName.split(' ')
            session['firstName'] = nameParts[0]
            session['userType'] = user['userType']
            g.user = user
            return redirect(url_for('user.profile'))

        flash(error)
    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('userId')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM User WHERE userId = ?', (user_id, )).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in g or g.user is None:
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
                hashed_passwd = bcrypt.hashpw(
                    passwd.encode('utf8'), bcrypt.gensalt())
                db.execute(
                    "INSERT INTO User (fullName, emailAddress, passwd, userType) VALUES (?, ?, ?, ?)",
                    (name, email, hashed_passwd, "USR"),
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
                return redirect(url_for('auth.login'))

        for error in errors:
            flash(error)
    return render_template('signup.html')


@bp.route('/register_seller', methods=['POST', 'GET'])
@login_required
def register_seller():
    print("Idhar")
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
                hashed_passwd = bcrypt.hashpw(
                    passwd.encode('utf8'), bcrypt.gensalt())
                db.execute(
                    "INSERT INTO User (fullName, emailAddress, passwd, userType) VALUES (?, ?, ?, ?)",
                    (name, email, hashed_passwd, "SLR"),
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
                return redirect(url_for('user.profile'))

        for error in errors:
            flash(error)
    print("Idhar")
    return render_template('register_seller.html')
