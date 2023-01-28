import os
import logging

from flask import Flask

def create_app(config = None):
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.from_mapping(config)

    app.config["TMP_PATH"] = os.path.join(app.instance_path, "tmp")
    try:
        os.makedirs(app.config["TMP_PATH"])
    except FileExistsError:
        pass

    app.logger.setLevel(logging.DEBUG)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    return app

