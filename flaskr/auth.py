from flask import Blueprint, render_template

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@bp.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')
