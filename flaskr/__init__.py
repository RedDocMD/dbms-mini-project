import os
from flask import Flask, render_template

user = {
    "fullName": "John Doe",
    "emailAddress": "xyz@gmail.com",
    "userType": "USR",
    "addressNames": [
        "1-a, Torana Apartments, Sahar Rd, Opp. P & T Colony, Andheri(e), Mumbai",
        "2nd Floor Ntc House, Nm Marg, Ballard Estate",
        "4, Jaya Niwas, Goraswadi, Near Milap Talkies, Malad (west)",    
    ],
    "orders":[
        {
            "numItems": 6,
            "cost": 1500
        },
        {
            "numItems": 7,
            "cost": 2000
        },
        {
            "numItems": 1,
            "cost": 2100
        },
        {
            "numItems": 8,
            "cost": 2300
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


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'data.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.get("/")
    @app.get("/index.html")
    def index():
        return render_template('orderSummary.html', order = order, user = user)

    from . import auth
    app.register_blueprint(auth.bp)
    from . import user
    app.register_blueprint(user.bp)

    return app
