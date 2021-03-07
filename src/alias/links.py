import pathlib
import sqlite3
from typing import Optional

import flask


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
            path to the SQLite database
        '''
        self._db = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES)

    def close(self):
        '''Close the underlying database connection.'''
        self._db.close()


def get_registry() -> LinksRegistry:
    '''Obtain the app's link registry instance.

    Returns
    -------
    LinksRegistry
        the registry instance
    '''
    if 'registry' in flask.g:
        return flask.g.registry

    registry_path = pathlib.Path(flask.current_app.instance_path) / 'links.sdb'
    flask.g.registry = LinksRegistry(registry_path)
    return flask.g.registry


def close_registry():
    '''Close the app's link registry if it is currently open.'''
    registry: Optional[LinksRegistry] = flask.g.pop('registry', None)
    if registry is not None:
        registry.close()
