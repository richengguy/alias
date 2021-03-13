import pytest

from alias import create_app, LinksRegistry


@pytest.fixture
def client(tmp_path):
    app = create_app(tmp_path)
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            dbfile = tmp_path / app.config['DATABASE_NAME']
            with LinksRegistry(dbfile) as registry:
                registry.initialize()
        yield client
