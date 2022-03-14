from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
from flaskr.auth import login_required


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if (request.method == 'POST') :
        print(request.form['type'])
        user_id = g.user['userId']
        db = get_db()
        if(request.form['type'] == 'Q') :
            prodId = request.form['prodId']
            sellerId = request.form['sellerId']
            newQ = request.form['newQ']
            db.execute(
                ('UPDATE Cart '
                'SET quantity = ? '
                'WHERE userId = ? AND prodId = ? AND sellerId = ?'), (newQ, user_id, prodId, sellerId))
        
        elif(request.form['type'] == 'R') :
            prodId = request.form['prodId']
            sellerId = request.form['sellerId']
            db.execute(
                ('DELETE FROM Cart '
                'WHERE userId = ? AND prodId = ? AND sellerId = ?'),(user_id, prodId, sellerId))
            )
            
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

    else:
        db = get_db()
        user_id = g.user['userId']

        productsData = db.execute(
            ('SELECT DISTINCT p.productId, p.productName, p.productDescription, c.quantity, sp.price, sp.discount, sp.sellerId  '
            'FROM Product p, Cart c, SellerProduct sp '
            'WHERE p.productId = c.productId AND c.userId = ? AND sp.productId = p.productId'), (user_id,)).fetchall()

        products = []
        prices = {}
        discounted_prices = {}

        for row in productsData:
            product = {
                'productId': row['productId'],
                'productName': row['productName'],
                'productDescription': row['productDescription'],
                'sellerId': row['sellerId']
            }
            products.append(product)
            price = row['price']
            discount = row['discount']
            prices[product['productId']] = price
            discounted_prices[product['productId']] = int(price *
                                                        (100.0 - discount) / 100.0)

        return render_template('cart.html',
                            products=products, prices=prices, discounted_prices=discounted_prices)


        

@bp.route('/wishlist', methods=['GET','POST'])
@login_required
def wishlist():
    if (request.method == 'POST') :
        user_id = g.user['userId']
        db = get_db()
        if(request.form['type'] == 'R') :
            prodId = request.form['prodId']

            db.execute(
                ('DELETE FROM Wishlist '
                'WHERE prodId = ? AND userId = ?'), (prodId, user_id))

            productsData = db.execute(
            ('SELECT DISTINCT p.productId, p.productName, p.productDescription  '
            'FROM Product p, Wishlist w '
            'WHERE p.productId = w.productId AND w.userId = ? AND w.productId = p.productId'), (user_id,)).fetchall()

            products = []

            for row in productsData:
                product = {
                    'productId': row['productId'],
                    'productName': row['productName'],
                    'productDescription': row['productDescription']
                }
                products.append(product)

            return render_template('wishlist.html',
                                products=products)
    else :
        db = get_db()
        user_id = g.user['userId']

        productsData = db.execute(
            ('SELECT DISTINCT p.productId, p.productName, p.productDescription  '
            'FROM Product p, Wishlist w '
            'WHERE p.productId = w.productId AND w.userId = ? AND w.productId = p.productId'), (user_id,)).fetchall()

        products = []

        for row in productsData:
            product = {
                'productId': row['productId'],
                'productName': row['productName'],
                'productDescription': row['productDescription']
            }
            products.append(product)

        return render_template('wishlist.html',
                            products=products)

