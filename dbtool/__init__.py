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


    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.oauth_login"
    login_manager.login_message = None
    login_manager.login_message_category = "info"

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    @login_manager.user_loader
    def load_user(email):  # pylint: disable=unused-variable
        """ Load user-object for logged in user

        `user_id` is stored in the session iff the user
        previously logged in successfully.
        So the user is authenticated automatically
        """
        if email not in app.config["USER"]:
            return

        user = main.User()
        user.id = email
        return user

    return app


