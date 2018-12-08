from flask import Flask

from app.xvideos import xvideos

DEFAULT_APP_NAME = 'TianKuiXing'

DEFAULT_MODULES = (
    (xvideos, '/xvideos'),
)


def setting_modules(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)


def init_app():
    app = Flask(DEFAULT_APP_NAME)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    setting_modules(app, DEFAULT_MODULES)
    return app
