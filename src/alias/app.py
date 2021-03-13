import os
import pathlib
from typing import Optional, Union

from flask import Flask, abort, redirect

from . import _dotenv  # noqa: F401
from .links import init_registry, get_registry


def create_app(instance_path: Optional[Union[str, pathlib.Path]] = None) -> Flask:
    '''Configure the WSGI web app instance.

    Parameters
    ----------
    instance_path : path-like
        the app's instance folder, optional

    Returns
    -------
    Flask
        the Flask web app instance
    '''
    if instance_path is None:
        if value := os.getenv('ALIAS_INSTANCE_PATH'):
            instance_path = pathlib.Path(value)

    if instance_path is None:
        flask_args = {'instance_relative_config': True}
    else:
        flask_args = {'instance_path': instance_path.resolve()}  # type: ignore

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
