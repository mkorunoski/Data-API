import os
import pathlib
from flask import Flask, make_response


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Provide default configuration parameters
    app.config.from_mapping(
        SECRET_KEY='dev',
        SUPPORTED_LOCALES=('en', 'de', 'fr', 'it', 'mk'),
        REDIS_DATABASE=0,
        SQLITE_DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    pathlib.Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from . import cache
    # Initialize the cache
    cache.init_app(app)

    from . import db
    # Initialize the database
    db.init_app(app)

    @app.route('/')
    def hello():
        return make_response('Hello, World!', 200)

    from . import data
    # Register the /data blueprint
    app.register_blueprint(data.bp)

    from . import consents
    # Register the /consents blueprint
    app.register_blueprint(consents.bp)

    return app
