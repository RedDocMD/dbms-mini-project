from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
from flaskr.auth import login_required
import json


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if (request.method == 'POST'):
        print(request.form['type'])
        user_id = g.user['userId']
        db = get_db()
        if(request.form['type'] == 'Q'):
            print("Quantity change...")
            prodId = request.form['prodId']
            sellerId = request.form['sellerId']
            newQ = request.form['newQ']
            db.execute(
                ('UPDATE Cart '
                 'SET quantity = ? '
                 'WHERE userId = ? AND productId = ? AND sellerId = ?'), (newQ, user_id, prodId, sellerId))
            db.commit()
            return "", 201

        elif(request.form['type'] == 'R'):
            print("Remove from cart...")
            prodId = request.form['prodId']
            sellerId = request.form['sellerId']
            db.execute(
                ('DELETE FROM Cart '
                 'WHERE userId = ? AND productId = ? AND sellerId = ?'), (user_id, prodId, sellerId))
            db.commit()
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
        prodId = request.args.get('prodId',"")
        sellerId = request.args.get('sellerId',"")

        if(prodId != ""):
            db.execute(
                ('DELETE FROM Cart '
                'WHERE userId = ? AND productId = ? AND sellerId = ?'), (user_id, prodId, sellerId))
            db.commit()
        
        all_prods = db.execute(
            ('SELECT DISTINCT p.productId, p.productName, p.productDescription, sp.sellerId, u.fullName, sp.price, sp.discount, c.quantity '
             'FROM Product p, SellerProduct sp, User u, Cart c '
             'WHERE p.productId = sp.productId AND sp.sellerId = u.userId '
             'AND c.userId = ? AND c.productId = p.productId AND c.sellerId = sp.sellerId '), (user_id, )).fetchall()

        products = []
        prices = {}
        discounted_prices = {}

        for row in all_prods:
            product = {}
            for key in row.keys():
                product[key] = row[key]
            products.append(product)
            price = row['price']
            discount = row['discount']
            prices[product['productId']] = price
            discounted_prices[product['productId']] = int(price *
                                                          (100.0 - discount) / 100.0)

        return render_template('cart.html', products=products, prices=prices, discounted_prices=discounted_prices)


@bp.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
    if (request.method == 'GET'):
        prodId = str(request.args.get('prodId', ""))
        db = get_db()
        user_id = g.user['userId']

        productsData = []
        if(prodId == ""):
            productsData = db.execute(
                ('SELECT DISTINCT p.productId, p.productName, p.productDescription  '
                 'FROM Product p, Wishlist w '
                 'WHERE p.productId = w.productId AND w.userId = ? AND w.productId = p.productId'), (user_id,)).fetchall()
        else:

            db.execute(
                ('DELETE FROM Wishlist '
                 'WHERE productId = ? AND userId = ?'), (prodId, user_id))

            db.commit()

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


@bp.route('/showseller', methods=['GET'])
@login_required
def showseller():
    if (request.method == 'GET'):
        user_id = g.user['userId']
        db = get_db()
        prodId = request.args['prodId']
        print(f"Reached here: {prodId}")
        # select sellers for that product
        # render the sellerlist.html and return the page
        # catch the response in the ajax reciever functions and render it in the empty div
        prod = db.execute(
            ('SELECT productId, productName, productDescription '
             'FROM Product WHERE productId = ?'), (prodId, )).fetchone()

        if prod is None:
            return redirect(url_for('user.wishlist'))

        sellers = db.execute(
            ('SELECT sp.sellerId, sp.productId, sp.discount, sp.price, u.fullName '
             'FROM SellerProduct sp, User u '
             'WHERE u.userId = sp.sellerId AND sp.productId = ? '), (prodId,)).fetchall()

        sellerinfo = []
        for row in sellers:
            price = row['price']
            discount = row['discount']
            discounted_price = int(price * (100.0 - discount) / 100.0)
            seller = {
                'sellerId': row['sellerId'],
                'name': row['fullName'],
                'prodId': row['productId'],
                'price': row['price'],
                'discountedPrice': discounted_price
            }
            sellerinfo.append(seller)

        return render_template("sellerlist.html", sellers=sellerinfo, productName=prod['productName'], productID=prod['productId'], productDescription=prod['productDescription'])
    else:
        return "", 200


@bp.route('/wishlisttocart', methods=['GET'])
@login_required
def wishlisttocart():
    if (request.method == 'GET'):
        user_id = g.user['userId']
        db = get_db()
        sellerId = request.args['seller']
        prodId = request.args['prod']

        # delete from wishlist
        # add to cart
        # return to wishlist
        db.execute(
            ('DELETE FROM Wishlist '
             'WHERE productId = ? AND userId = ? '), (prodId, user_id))
        db.commit()
        db.execute(
            ('INSERT INTO Cart '
             'VALUES (?,?,?,1) '), (user_id, prodId, sellerId))
        db.commit()

        return redirect(url_for('user.wishlist'))
    else:
        return redirect(url_for('user.wishlist'))


@bp.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
    if (request.method == 'POST'):
        user_id = g.user['userId']
        db = get_db()
        if (request.form['type'] == 'IC'):
            # check if already there then increment quantity or insert if not there
            prodId = request.form['prodId']
            sellerId = request.form['sellerId']

            db.execute(
                ('INSERT INTO Cart '
                 'VALUES (?,?,?,1) '
                 'ON CONFLICT(userId, productId, sellerId) '
                 'DO UPDATE SET quantity = quantity + 1 '), (user_id, prodId, sellerId)
            )
            db.commit()
            return "", 200
        elif (request.form['type'] == 'IW'):
            prodId = request.form['prodId']

            db.execute(
                ('INSERT OR IGNORE INTO Wishlist '
                 'VALUES (?,?) '), (user_id, prodId)
            )
            db.commit()
            return "", 200
        else:
            print("WARNING : Invalid request.")
            return "", 200
    else:
        db = get_db()

        search_key = str(request.args.get('searchStr', ""))
        print(search_key)
        search_term = '%' + search_key + '%'
        print(search_term)

        all_prods = []

        if(search_key == ""):
            all_prods = db.execute(
                ('SELECT DISTINCT p.productId, p.productName, p.productDescription, sp.sellerId, u.fullName, sp.price, sp.discount '
                 'FROM Product p, SellerProduct sp, User u '
                 'WHERE p.productId = sp.productId AND sp.sellerId = u.userId ')).fetchall()
        else:
            all_prods = db.execute(
                ('SELECT p.productId, p.productName, p.productDescription, sp.sellerId, u.fullName, sp.price, sp.discount '
                 'FROM Product p, SellerProduct sp, User u '
                 'WHERE p.productName LIKE ? AND p.productId = sp.productId AND sp.sellerId = u.userId '), (search_term,)).fetchall()

        products = []
        prices = {}
        discounted_prices = {}

        for row in all_prods:
            product = {
                'productId': row['productId'],
                'productName': row['productName'],
                'productDescription': row['productDescription'],
                'sellerId': row['sellerId'],
                'sellerName': row['fullName']
            }
            products.append(product)
            price = row['price']
            discount = row['discount']
            prices[product['productId']] = price
            discounted_prices[product['productId']] = int(price *
                                                          (100.0 - discount) / 100.0)

        return render_template('browse.html', products=products, prices=prices, discounted_prices=discounted_prices, searchStr=search_key)


# @bp.route('/search', methods=['GET'])
# @login_required
# def search():
#     #if (request.method == 'GET') :
#     db = get_db()
#     print(request.form)
#     search_key = str(request.args.get('searchStr',""))
#     print(search_key)
#     search_term = '%' + search_key + '%'
#     print(search_term)

#     all_prods = db.execute(
#         ('SELECT p.productId, p.productName, p.productDescription, sp.sellerId, u.fullName, sp.price, sp.discount '
#         'FROM Product p, SellerProduct sp, User u '
#         'WHERE p.productName LIKE ? AND p.productId = sp.productId AND sp.sellerId = u.userId '), (search_term,)).fetchall()

#     products = []
#     prices = {}
#     discounted_prices = {}

#     for row in all_prods:
#         product = {
#             'productId': row['productId'],
#             'productName': row['productName'],
#             'productDescription': row['productDescription'],
#             'sellerId': row['sellerId'],
#             'sellerName': row['fullName']
#         }
#         products.append(product)
#         price = row['price']
#         discount = row['discount']
#         prices[product['productId']] = price
#         discounted_prices[product['productId']] = int(price *
#                                                     (100.0 - discount) / 100.0)

#     return render_template('browse.html', products=products, prices=prices, discounted_prices=discounted_prices, searchStr=search_key)


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    # user = {
    #     "fullName": "John Doe",
    #     "emailAddress": "xyz@gmail.com",
    #     "userType": "ADM",
    #     "sellers": [
    #         {
    #             "name": "Aaditya",
    #             "seller_id": 1
    #         },
    #         {
    #             "name": "Deep",
    #             "seller_id": 2
    #         }
    #     ]
    # }
    # user = {
    #     "fullName": "John Doe",
    #     "emailAddress": "xyz@gmail.com",
    #     "userType": "USR",
    #     "addressNames": [
    #         {
    #             "addressName": "1-a, Torana Apartments, Sahar Rd, Opp. P & T Colony, Andheri(e), Mumbai",
    #             "address_id": 1
    #         },
    #         {
    #             "addressName": "2nd Floor Ntc House, Nm Marg, Ballard Estate",
    #             "address_id": 2
    #         },
    #         {
    #             "addressName": "4, Jaya Niwas, Goraswadi, Near Milap Talkies, Malad (west)",
    #             "address_id": 3
    #         }

    #     ],
    #     "orders":[
    #         {
    #             "order_id": 1,
    #             "numItems": 6,
    #             "cost": 1500
    #         },
    #         {
    #             "order_id": 2,
    #             "numItems": 7,
    #             "cost": 2000
    #         },
    #         {
    #             "order_id": 3,
    #             "numItems": 1,
    #             "cost": 2100
    #         },
    #         {
    #             "order_id": 4,
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
    #             "product_id": 1,
    #         },
    #         {
    #             "name": "Kurkure",
    #             "product_id": 2,
    #         },
    #         {
    #             "name": "Crescent City",
    #             "product_id": 3,
    #         },
    #         {
    #             "name": "Harry Potter",
    #             "product_id": 4,
    #         },
    #     ],
    # }

    # return render_template('profile.html', user = user)
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
        user['userId'] = userData['userId']

        if userType == 'USR':
            addresses = []
            addressData = db.execute((
                'SELECT * '
                'FROM UserAddress a '
                'WHERE a.userId = ?'
            ), (user_id,)).fetchall()

            for row in addressData:
                addresses.append({
                    "addressName": row['addressName'],
                    "address_id": row['addressId']
                })
            user['addressNames'] = addresses

            user['orders'] = []
            orderData = db.execute((
                'SELECT orderId, totalCost '
                'FROM Orders '
                'WHERE userId = ?'
            ), (user_id, )).fetchall()
            for row in orderData:
                orderId = row['orderId']
                orderProductData = db.execute((
                    'SELECT COUNT(*) AS numItems '
                    'FROM OrderProduct '
                    'WHERE orderId = ?'
                ), (orderId, )).fetchone()
                numItems = orderProductData["numItems"]
                user['orders'].append({
                    "numItems": numItems,
                    "order_id": orderId,
                    "cost": row["totalCost"]
                })
            return render_template('profile.html', user=user)
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
            return render_template('profile.html', user=user)
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
            return render_template('profile.html', user=user)
    flash(error)


@bp.route('/deleteSeller', methods=['POST'])
@login_required
def deleteSeller():
    if request.method == 'POST':
        try:
            seller_id = request.form['seller_id']
        except:
            return ""
        db = get_db()

        db.execute((
            'DELETE '
            'FROM User '
            'WHERE userId = ?'
        ), (seller_id,))
        db.commit()
        return "", 201


@bp.route('/addAddress', methods=['GET', 'POST'])
@login_required
def addAddress():
    if request.method == 'POST':
        address = request.form['address']

        db = get_db()

        errors = []
        if not address:
            errors.append("Address is required")

        if not errors:
            try:
                user_id = g.user['userId']

                oldMaxAddressId = db.execute(
                    "SELECT MAX(addressId) FROM UserAddress").fetchone()[0]
                if oldMaxAddressId is None:
                    oldMaxAddressId = 0
                db.execute(
                    "INSERT INTO UserAddress (userId, addressId, addressName) VALUES (?, ?, ?)",
                    (user_id, oldMaxAddressId + 1, address),
                )
                db.commit()
            except Exception as r:
                errors.append("Error in inserting new address")
            else:
                return redirect(url_for('user.profile'))

        for error in errors:
            flash(error)
    return render_template('addAddress.html')


@bp.route('/editAddress/<address_id>', methods=['GET', 'POST'])
@login_required
def editAddress(address_id):
    db = get_db()
    if request.method == 'POST':
        address = request.form['address']

        db = get_db()

        errors = []
        if not address:
            errors.append("Address is required")

        if not errors:
            try:
                db.execute(
                    'UPDATE UserAddress SET addressName = ? WHERE userId = ? AND addressId = ?',
                    (address, g.user['userId'], address_id)
                )
                db.commit()
            except Exception as r:
                errors.append("Error in inserting new address")
            else:
                return redirect(url_for('user.profile'))

        for error in errors:
            flash(error)

    addressData = db.execute(
        'SELECT * '
        'FROM UserAddress AS ua '
        'WHERE ua.userId = ? AND ua.addressId = ?', (g.user['userId'], address_id)).fetchone()

    print(addressData["addressName"])
    return render_template('editAddress.html', address=addressData)


@bp.route('/deleteAddress', methods=['POST'])
@login_required
def deleteAddress():
    if request.method == 'POST':
        try:
            address_id = request.form['address_id']
            user_id = g.user['userId']
        except:
            return ""
        db = get_db()

        db.execute((
            'DELETE '
            'FROM UserAddress '
            'WHERE userId = ? and addressId = ?'
        ), (user_id, address_id,))
        db.commit()
        return "", 201


@bp.route('/deleteProduct', methods=['POST'])
@login_required
def deleteItem():
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
