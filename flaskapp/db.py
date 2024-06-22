import sqlite3

import click
from flask import current_app, g

# Stol EHEM copied from flask tutorial guide
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('database-schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('initialize-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def set_app(app):
    app.teardown_appcontext(close_db) # close db connection after return the response
    app.cli.add_command(init_db_command) # add the new cli command