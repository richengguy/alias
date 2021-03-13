from click.testing import CliRunner
import pytest

from alias import default_config, LinksRegistry
from alias.cli import main


@pytest.fixture
def runner(tmp_path):
    runner = CliRunner(env={
        'ALIAS_INSTANCE_PATH': tmp_path.as_posix()
    })
    result = runner.invoke(main, 'init')
    assert result.exit_code == 0
    return runner


@pytest.fixture
def dbfile(tmp_path):
    return tmp_path / default_config.DATABASE_NAME


class TestCli:
    def test_add_links(self, runner, dbfile):
        result = runner.invoke(main, ['add', 'shortcut', 'https://shortcut.example.com'])
        assert result.exit_code == 0

        with LinksRegistry(dbfile) as registry:
            assert registry.get('shortcut') == 'https://shortcut.example.com'

    def test_remove_links(self, runner, dbfile):
        with LinksRegistry(dbfile) as registry:
            registry.add('shortcut', 'https://shortcut.example.com')

        result = runner.invoke(main, ['remove', 'shortcut'])
        assert result.exit_code == 0

        with LinksRegistry(dbfile) as registry:
            assert registry.num_links == 0

    def test_duplicate_insert_has_nonzero_exit(self, runner):
        result = runner.invoke(main, ['add', 'shortcut', 'https://shortcut.example.com'])
        assert result.exit_code == 0

        result = runner.invoke(main, ['add', 'shortcut', 'https://other.example.com'])
        assert result.exit_code == 1

    def test_nonexistant_remove_has_nonzero_exit(self, runner):
        result = runner.invoke(main, ['remove', 'shortcut'])
        assert result.exit_code == 1
