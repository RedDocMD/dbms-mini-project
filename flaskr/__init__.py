import os
from flask import Flask, redirect, url_for


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
    def index():
        return redirect(url_for('user.profile'))

    from . import auth
    app.register_blueprint(auth.bp)
    from . import user
    app.register_blueprint(user.bp)
    from . import order
    app.register_blueprint(order.bp)
    from . import item
    app.register_blueprint(item.bp)

    return app
