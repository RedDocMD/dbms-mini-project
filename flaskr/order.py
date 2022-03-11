from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.auth import login_required
from flaskr.db import get_db
import functools


bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('', methods=['GET'])
@login_required
def order():
    if request.method == 'GET':
        order_id = request.args.get('order_id')
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

        return render_template('orderSummary.html', user = user, order = order)
        
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM User WHERE emailAddress = ?', (email,)).fetchone()
        if user is None:
            error = "Username doesn't exist"
        elif passwd != user['passwd']:
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['userId'] = user['userId']
            fullName = user['fullName']
            nameParts = fullName.split(' ')
            session['firstName'] = nameParts[0]
            g.user = user
            return redirect(url_for('index.html'))

        flash(error)
    return render_template('login.html')