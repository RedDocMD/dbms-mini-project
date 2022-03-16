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


@bp.route('/add', methods=['GET'])
@login_required
def add():
    return render_template('add_item.html')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if g.user['userType'] != 'SLR':
        return redirect('/')
    if request.method == 'POST':
        db = get_db()
        user_id = g.user['userId']

        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        disc = request.form['discount']
        qty = request.form['quantity']

        errors = []
        try:
            prod_cursor = db.execute(
                'INSERT INTO Product (productName, productDescription) VALUES (?, ?)', (name, desc))
            prod_id = prod_cursor.lastrowid
            db.execute(
                'INSERT INTO SellerProduct (productId, sellerId, price, discount, quantity) VALUES (?, ?, ?, ?, ?)',
                (prod_id, user_id, price, disc, qty))
            db.commit()
        except db.IntegrityError as e:
            errors.append(f'Failed to add {e}')
        else:
            return redirect(url_for('user.profile'))

        for error in errors:
            flash(error)
    return render_template('add_new_item.html')


@bp.route('/assign', methods=['GET', 'POST'])
@login_required
def assign():
    db = get_db()
    if request.method == 'POST':
        selected_id = request.form['selected_product']
        print(f'Selected_id = {selected_id}')
        return redirect(url_for('item.assign_values', product_id=selected_id))
    products = db.execute('SELECT * FROM Product').fetchall()
    return render_template('assign_item.html', products=products)


@bp.route('/assign/<product_id>', methods=['GET', 'POST'])
@login_required
def assign_values(product_id):
    db = get_db()
    if request.method == 'POST':
        price = request.form['price']
        disc = request.form['discount']
        qty = request.form['quantity']
        errors = []
        try:
            db.execute(
                'INSERT INTO SellerProduct (productId, sellerId, price, discount, quantity) VALUES (?, ?, ?, ?, ?)',
                (product_id, g.user['userId'], price, disc, qty))
            db.commit()
        except db.IntegrityError as e:
            errors.append(f'Failed to add {e}')
        else:
            return redirect(url_for('user.profile'))
    product = db.execute(
        'SELECT * FROM Product WHERE productId = ?', (product_id, )).fetchone()
    return render_template('assign_item_data.html', product=product)


@bp.route('/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit(product_id):
    db = get_db()
    if request.method == 'POST':
        pass
    product = db.execute(
        'SELECT * FROM Product WHERE productId = ?', (product_id, )).fetchone()
    seller_data = db.execute(
        'SELECT price, discount, quantity FROM SellerProduct WHERE productId = ? AND sellerId = ?',
        (product_id, g.user['userId'])).fetchone()
    return render_template('edit_item.html', product=product, seller_data=seller_data)
