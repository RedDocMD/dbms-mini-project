from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
from flaskr.auth import login_required


bp = Blueprint('item', __name__, url_prefix='/item')


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        try:
            product_id = request.form['product_id']
            user_id = g.user['userId']
        except:
            return ""
        db = get_db()

        db.execute((
            'DELETE '
            'FROM SellerProduct '
            'WHERE sellerId = ? and productId = ?'
        ), (user_id, product_id,))
        db.commit()
        return "", 201


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        pass
    return render_template('add_item.html')
