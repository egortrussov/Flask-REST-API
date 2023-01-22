import os

from flask import Flask, g

from .db import init_db
from .db.db import global_init_db

from .extensions.routes_extension import register_blueprints

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    
    
    init_db.init_app(app)
    global_init_db(os.path.join(app.instance_path, 'db.sqlite'))

    register_blueprints(app)

    return app