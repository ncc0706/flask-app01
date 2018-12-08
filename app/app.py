from flask import Flask


def register_blueprints(app):
    """
    蓝图注册
    :param app:
    :return:
    """
    from app.api.v1.video import video

    app.register_blueprint(video)


def init_app():
    app = Flask(__name__)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')

    register_blueprints(app)

    return app
