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
        ('SELECT p.productId, p.productName, p.productDescription, c.quantity, sp.price, sp.discount  '
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


@bp.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
    db = get_db()
    user_id = g.user['userId']

    products = db.execute(
        (
            'SELECT p.productId, p.productName, p.productDescription '
            'FROM Wishlist w, Product p '
            'WHERE p.productId = w.productId AND w.userId = ?'
        ), (user_id, )
    ).fetchall()

    return render_template('wishlist.html', products=products)


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = {
        "fullName": "John Doe",
        "emailAddress": "xyz@gmail.com",
        "userType": "ADM",
        "sellers": [
            {
                "name": "Aaditya",
                "seller_id": 1
            },
            {
                "name": "Deep",
                "seller_id": 2
            }
        ]
    }

    return render_template('profile.html', user = user)
    db = get_db()
    user_id = g.user['userId']

    user = {}

    userData = db.execute((
        'SELECT * '
        'FROM USER u '
        'WHERE u.userId = ?'
    ), (user_id,)).fetchone()

    error = None

    if user is None:
        error = "User doesn't exist"
    
    if error is None:
        user['fullName'] = userData['fullName']
        user['emailAddress'] = userData['emailAddress']
        userType = userData['userType']
        user['userType'] = userType

        if userType == 'USR':
            addresses = []
            addressData = db.execute((
                'SELECT * '
                'FROM UserAddress a '
                'WHERE a.userId = ?'
            ), (user_id,)).fetchall()

            for row in addressData:
                addresses.append(row['addressName'])
            user['addressNames'] = addresses

            user['orders'] = []
            return render_template('profile.html', user = user)
        elif userType == 'SLR':
            items = []
            itemData = db.execute((
                'SELECT p.productName, p.productId '
                'FROM SellerProduct sp, Product p '
                'WHERE sp.sellerId = ? AND p.productId = sp.productId'
            ), (user_id,)).fetchall()

            for row in itemData:
                items.append(
                    {
                        "name": row["productName"],
                        "product_id": row["productId"]
                    }
                )
            user['items'] = items
            return render_template('profile.html', user = user)
        elif userType == 'ADM':
            sellers = []
            sellerData = db.execute((
                'SELECT u.userId, u.fullName '
                'FROM User u '
                'WHERE u.userType = "SLR"'
            )).fetchall()

            for row in sellerData:
                sellers.append(
                    {
                        "name": row["fullName"],
                        "seller_id": row["userId"]
                    }
                )
            user['sellers'] = sellers
            return render_template('profile.html', user = user)
    flash(error)
    
    # user = {
    #     "fullName": "John Doe",
    #     "emailAddress": "xyz@gmail.com",
    #     "userType": "USR",
    #     "addressNames": [
    #         "1-a, Torana Apartments, Sahar Rd, Opp. P & T Colony, Andheri(e), Mumbai",
    #         "2nd Floor Ntc House, Nm Marg, Ballard Estate",
    #         "4, Jaya Niwas, Goraswadi, Near Milap Talkies, Malad (west)",    
    #     ],
    #     "orders":[
    #         {
    #             "numItems": 6,
    #             "cost": 1500
    #         },
    #         {
    #             "numItems": 7,
    #             "cost": 2000
    #         },
    #         {
    #             "numItems": 1,
    #             "cost": 2100
    #         },
    #         {
    #             "numItems": 8,
    #             "cost": 2300
    #         },
    #     ],
    # }

    # user = {
    #     "fullName": "John Doe",
    #     "emailAddress": "xyz@gmail.com",
    #     "userType": "SLR",
    #     "items":[
    #         {
    #             "name": "Lays",
    #         },
    #         {
    #             "name": "Kurkure",
    #         },
    #         {
    #             "name": "Crescent City",
    #         },
    #         {
    #             "name": "Harry Potter",
    #         },
    #     ],
    # }

