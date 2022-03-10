from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
from flaskr.auth import login_required


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/cart', methods=['GET'])
@login_required
def cart():
    db = get_db()
    user_id = g.user['userId']

    productsData = db.execute(
        ('SELECT DISTINCT p.productId, p.productName, p.productDescription, c.quantity, sp.price, sp.discount  '
         'FROM Product p, Cart c, SellerProduct sp '
         'WHERE p.productId = c.productId AND c.userId = ? AND sp.productId = p.productId'), (user_id,)).fetchall()

    products = []
    prices = {}
    discounted_prices = {}

    for row in productsData:
        product = {
            'productId': row['productId'],
            'productName': row['productName'],
            'productDescription': row['productDescription']
        }
        products.append(product)
        price = row['price']
        discount = row['discount']
        prices[product['productId']] = price
        discounted_prices[product['productId']] = int(price *
                                                      (100.0 - discount) / 100.0)

    return render_template('cart.html',
                           products=products, prices=prices, discounted_prices=discounted_prices)
