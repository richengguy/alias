import os
import pathlib

from flask import Flask

from . import _dotenv  # noqa: F401


def create_app() -> Flask:
    '''Configure the WSGI web app instance.

    Returns
    -------
    Flask
        the Flask web app instance
    '''
    if value := os.getenv('ALIAS_INSTANCE_PATH'):
        path = pathlib.Path(value)
        flask_args = {'instance_path': path.resolve()}
    else:
        flask_args = {'instance_relative_config': True}  # type: ignore

    from .links import init_registry

    app = Flask(__name__.split('.')[0], **flask_args)  # type: ignore
    app.config.from_object('alias.default_config')
    init_registry(app)

    @app.route('/')
    def index():
        return 'Link Aliasing'

    return app
