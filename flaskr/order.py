from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.auth import login_required
from flaskr.db import get_db
import functools


bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/<order_id>', methods=['GET'])
@login_required
def order(order_id):
    if request.method == 'GET':
        print(order_id)
        user = {
            "fullName": "John Doe",
            "emailAddress": "xyz@gmail.com",
            "userType": "ADM",
            "sellers":[
                {
                    "name": "John Cena",
                },
                {
                    "name": "Undertaker",
                },
                {
                    "name": "CM Punk",
                },
                {
                    "name": "Batista",
                },
            ],
        }

        order = {
            "items": [
                {
                    "name": "Lays",
                    "quantity": 2,
                    "cost": 1000,
                },
                {
                    "name": "Kurkure",
                    "quantity": 2,
                    "cost": 2000,
                },
                {
                    "name": "Novel",
                    "quantity": 1,
                    "cost": 3000,
                },
            ],
            "cost": 6000,
            "address": "1-a, Torana Apartments, Sahar Rd, Opp. P & T Colony, Andheri(e), Mumbai",
        }

        db = get_db()
        user_id = g.user['userId']
        user = {}
        order = {}

        userData = db.execute((
        'SELECT * '
        'FROM USER u '
        'WHERE u.userId = ?'
        ), (user_id,)).fetchone()

        user['fullName'] = userData['fullName']
        user['emailAddress'] = userData['emailAddress']
        addressData = db.execute(
            'SELECT ua.addressName '
            'FROM Orders AS o, UserAddress as ua '
            'WHERE o.orderId = ? AND ua.userId = ? AND ua.addressId = o.addressId'
        ,(order_id, user_id, )).fetchone()

        order['address'] = addressData['addressName']

        orderData = db.execute(
            'SELECT * '
            'FROM Orders '
            'WHERE orderId = ?'
        , (order_id, )).fetchone()
        
        order['cost'] = orderData['totalCost']

        orderProductData = db.execute(
            'SELECT * '
            'FROM OrderProduct '
            'WHERE orderId = ? '
        , (order_id)).fetchall()

        order['items'] = []
        for row in orderProductData:
            order['items'].append({
                "name": row["productName"],
                "quantity": row["quantity"],
                "cost": row["discountPrice"],
            })



        return render_template('orderSummary.html', user = user, order = order)
        

@bp.route('/deleteOrder', methods=['POST'])
@login_required
def deleteOrder():
    if request.method == 'POST':
        try:
            order_id = request.form['order_id']
        except:
            return ""
        db = get_db()
        
        db.execute((
            'DELETE '
            'FROM Orders '
            'WHERE orderId = ?'
        ), (order_id,))

        db.execute((
            'DELETE '
            'FROM OrderProduct '
            'WHERE orderId = ?'
        ), (order_id,))
        db.commit()
        return "", 201