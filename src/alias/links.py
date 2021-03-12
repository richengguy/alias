import pathlib
import sqlite3
from typing import NamedTuple, Optional

import flask


class LinkEntry(NamedTuple):
    alias: str
    href: str


class LinksRegistry:
    '''A key-value store that maps a short name to a URL.

    The registry is used to find the URL that maps to a particular alias.  The
    mapping is stored on disk as a single table within an SQLite database.
    '''
    def __init__(self, dbpath: pathlib.Path):
        '''Initialize a new registry instance.

        Parameters
        ----------
        dbpath : pathlib.Path
            path to the SQLite database file
        '''
        self._db = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES)
        self._db.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._db.close()

    def close(self):
        '''Close the underlying database connection.'''
        self._db.close()

    def initialize(self):
        '''Initialize the SQLite database.

        This is a destructive operation that will remove *all* data in the
        database.  It should be used to either create a new database or reset an
        existing one.
        '''
        from importlib import resources
        schema = resources.read_text('alias', 'schema.sql')
        self._db.executescript(schema)

    def add(self, alias: str, url: str):
        '''Add an alias into the registry.

        Parameters
        ----------
        alias : str
            the link alias; this *must* be unique
        url : str
            the url the alias points to

        Raises
        ------
        KeyError
            if the key already exists
        ValuError
            if there was some other error
        '''
        try:
            with self._db:
                self._db.execute('INSERT INTO links VALUES (?, ?)', (alias, url))
        except sqlite3.IntegrityError as exc:
            if str(exc).startswith('UNIQUE constraint'):
                raise KeyError(f'Could not add \'{alias}\'; it already exists.')
            else:
                raise ValueError(f'Could not add \'{alias}\'.') from exc

    def remove(self, alias: str):
        '''Remove an alias from the registry.

        Parameters
        ----------
        alias : str
            alias to remove
        '''
        with self._db:
            rows = self._db.execute('DELETE FROM links WHERE shortcut == (?)', (alias,))
            if rows.rowcount == 0:
                raise KeyError(f'There is no \'{alias}\' in the registry.')

    def list(self) -> list[LinkEntry]:
        '''List all of the available links.

        Returns
        -------
        list of `(alias, url)` pairs
            list of the stored aliases
        '''
        rows = self._db.execute('SELECT * FROM links')
        return list(LinkEntry(r['shortcut'], r['href']) for r in rows)


def init_registry(app: flask.Flask):
    '''Initialize the registry with the Flask app instance.

    Parameters
    ----------
    app : flask.Flask
        the flask app context (i.e. instance)
    '''
    app.teardown_appcontext(close_registry)


def get_registry() -> LinksRegistry:
    '''Obtain the app's link registry instance.

    Returns
    -------
    LinksRegistry
        the registry instance
    '''
    if 'registry' in flask.g:
        return flask.g.registry

    dbname = flask.current_app.config['DATABASE_NAME']
    registry_path = pathlib.Path(flask.current_app.instance_path) / dbname
    flask.g.registry = LinksRegistry(registry_path)
    return flask.g.registry


def close_registry(exception=None):
    '''Close the app's link registry if it is currently open.'''
    registry: Optional[LinksRegistry] = flask.g.pop('registry', None)
    if registry is not None:
        registry.close()
