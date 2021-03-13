from flask import Flask
from flask.testing import FlaskClient
import pytest

from alias import create_app, LinksRegistry


@pytest.fixture
def app(tmp_path) -> Flask:
    app = create_app(tmp_path)
    app.config['TESTING'] = True

    with app.app_context():
        dbfile = tmp_path / app.config['DATABASE_NAME']
        with LinksRegistry(dbfile) as registry:
            registry.initialize()

    return app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

    # app = create_app(tmp_path)
    # app.config['TESTING'] = True

    # with app.test_client() as client:
    #     with app.app_context():
    #         dbfile = tmp_path / app.config['DATABASE_NAME']
    #         with LinksRegistry(dbfile) as registry:
    #             registry.initialize()
    #     yield client
