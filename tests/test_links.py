import pytest

from alias import LinksRegistry


@pytest.fixture
def links_registry(tmp_path):
    dbfile = tmp_path / 'links.sdb'
    with LinksRegistry(dbfile) as registry:
        registry.initialize()
        yield registry


class TestLinksRegistry:
    def test_add_links(self, links_registry):
        links_registry.add('shortcut', 'https://shortcut.example.com')
        assert links_registry.get('shortcut') == 'https://shortcut.example.com'
        assert links_registry.num_links == 1

    def test_remove_links(self, links_registry):
        links_registry.add('first', 'https://first.example.com')
        links_registry.add('second', 'https://second.example.com')
        assert links_registry.num_links == 2

        links_registry.remove('second')
        assert links_registry.num_links == 1

    def test_list_all_links(self, links_registry):
        expected = [(f'link-{i+1}', f'https://{i+1}.example.com') for i in range(5)]

        for alias, href in expected:
            links_registry.add(alias, href)

        assert links_registry.list() == expected

    def test_error_on_duplicate_insert(self, links_registry):
        links_registry.add('shortcut', 'https://shortcut.example.com')
        assert links_registry.num_links == 1

        with pytest.raises(KeyError):
            links_registry.add('shortcut', 'https://shortcut.example.com')
        assert links_registry.num_links == 1

    def test_error_on_get_missing_alias(self, links_registry):
        assert links_registry.num_links == 0
        with pytest.raises(KeyError):
            links_registry.get('shortcut')

    def test_error_on_remove_missing_alias(self, links_registry):
        assert links_registry.num_links == 0
        with pytest.raises(KeyError):
            links_registry.remove('shortcut')
