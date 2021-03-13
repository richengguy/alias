from alias.app import get_registry


class TestApp:
    def test_shortcut_issues_301_redirect(self, app, client):
        with app.app_context():
            registry = get_registry()
            registry.add('shortcut', 'https://shortcut.example.com')

        resp = client.get('/shortcut')
        assert resp.status_code == 301
        assert resp.headers['Location'] == 'https://shortcut.example.com'

    def test_missing_alias_returns_404(self, client):
        resp = client.get('/')
        assert resp.status_code == 404

        resp = client.get('/shortcut')
        assert resp.status_code == 404
