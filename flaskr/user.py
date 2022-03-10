from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, flash, session)
from flaskr.db import get_db
from flaskr.auth import login_required


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/cart', methods=['GET'])
@login_required
def cart():
    products = []
    prices = {}
    discountedPrices = {}
    return render_template('cart.html',
                           products=products, prices=prices, discountedPrices=discountedPrices)
