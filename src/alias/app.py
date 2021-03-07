import pathlib

from flask import Flask


def create_app() -> Flask:
    '''Initialize a new 'alias' app instance.

    Returns
    -------
    Flask
        the Flask web app instance
    '''
    app = Flask(__name__, instance_relative_config=True)
    instance_path = pathlib.Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    @app.route('/')
    def index():
        return 'Link Aliasing'

    return app
