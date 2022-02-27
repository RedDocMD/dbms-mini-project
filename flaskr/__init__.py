import os
from flask import Flask, render_template


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
        return render_template('index.html')

    return app
