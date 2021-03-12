import pathlib
from typing import Tuple, Union

import click

from . import _dotenv  # noqa: F401
from ._version import version
from .app import create_app
from .links import LinksRegistry


def _get_app_info() -> Tuple[pathlib.Path, pathlib.Path]:
    app = create_app()
    with app.app_context():
        instance_path = pathlib.Path(app.instance_path)
        dbfile = instance_path / app.config['DATABASE_NAME']

    return instance_path, dbfile


@click.group()
def main():
    '''Manage the contents of an 'alias' web app.'''
    click.echo(f'Alias v{version}')


@main.command('init')
@click.option('--instance-path', envvar='ALIAS_INSTANCE_PATH',
              help='Path to the app\'s runtime folder.',
              type=click.Path(file_okay=False, dir_okay=True))
def initialize(instance_path: Union[str, pathlib.Path]):
    '''Initialize the 'alias' web app.'''
    instance_path, dbfile = _get_app_info()

    try:
        click.echo(f'Creating instance folder at {instance_path}...', nl=False)
        instance_path.mkdir(parents=True, exist_ok=False)
        click.secho('DONE', fg='green', bold=True)
    except FileExistsError:
        click.secho('EXISTS', bold=True)

    with LinksRegistry(dbfile) as links:
        click.echo('Initializing database...', nl=False)
        links.initialize()
        click.secho('DONE', fg='green', bold=True)


@main.command('add')
@click.argument('alias')
@click.argument('url')
def add_link(alias: str, url: str):
    '''Add an alias link.

    The alias is comprise of two parts: the link URL and the ALIAS used to
    access it.  An alias instance issues 301 HTTP redirects so that, e.g.
    `https://alias.example.com/search` maps to `https://www.google.com`.  In
    this case, 'search' is the ALIAS and 'https://www.google.com' is the URL.
    '''
    _, dbfile = _get_app_info()
    with LinksRegistry(dbfile) as links:
        click.echo(f'Adding {alias} -> {url}...', nl=False)
        links.add(alias, url)
        click.secho('DONE', fg='green', bold=True)


@main.command('list')
def list_aliases():
    '''List all stored aliases.'''
    _, dbfile = _get_app_info()

    rowfmt = '{:<12} {:}'
    with LinksRegistry(dbfile) as links:
        click.echo(rowfmt.format('Shortcut', 'URL'))
        click.echo(rowfmt.format('--------', '---'))
        for entry in links.list():
            click.echo(rowfmt.format(entry.alias, entry.href))


if __name__ == '__main__':
    main()
