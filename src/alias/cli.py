import pathlib
from typing import Union

import click
import flask

from . import _dotenv  # noqa: F401
from ._version import version
from .app import create_app
from .links import LinksRegistry


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
    app = create_app()
    with app.app_context():
        instance_path = pathlib.Path(app.instance_path)
        dbfile = instance_path / app.config['DATABASE_NAME']

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


if __name__ == '__main__':
    main()
