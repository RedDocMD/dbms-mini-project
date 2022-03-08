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
            try:
                db.execute(
                    "INSERT INTO User (fullName, emailAddress, passwd, userType) VALUES (?, ?, ?, ?)",
                    (name, email, passwd, "USR"),
                )
                userId = db.execute(
                    f'SELECT userId FROM User WHERE emailAddress = "{email}"').fetchone()[0]
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
