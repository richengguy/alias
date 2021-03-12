import os
import pathlib

from flask import Flask, abort, redirect

from . import _dotenv  # noqa: F401
from .links import init_registry, get_registry


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

    app = Flask(__name__.split('.')[0], **flask_args)  # type: ignore
    app.config.from_object('alias.default_config')
    init_registry(app)

    @app.route('/<string:alias>')
    def index(alias: str):
        registry = get_registry()
        try:
            url = registry.get(alias)
            return redirect(url, code=301)
        except KeyError:
            abort(404)

    return app
