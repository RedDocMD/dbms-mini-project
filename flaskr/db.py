import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
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
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def clear_tables():
    db = get_db()
    db.execute("DELETE FROM User")
    db.execute("DELETE FROM Product")
    db.execute("DELETE FROM Wishlist")
    db.execute("DELETE FROM Cart")
    db.execute("DELETE FROM UserAddress")
    db.execute("DELETE FROM SellerProduct")
    db.execute("DELETE FROM Orders")
    db.execute("DELETE FROM OrderProduct")
    db.commit()


def clear_db():
    db = get_db()
    db.execute("DROP TABLE IF EXISTS User")
    db.execute("DROP TABLE IF EXISTS Product")
    db.execute("DROP TABLE IF EXISTS Wishlist")
    db.execute("DROP TABLE IF EXISTS Cart")
    db.execute("DROP TABLE IF EXISTS UserAddress")
    db.execute("DROP TABLE IF EXISTS SellerProduct")
    db.execute("DROP TABLE IF EXISTS Orders")
    db.execute("DROP TABLE IF EXISTS OrderProduct")
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create database and run schema.sql"""
    init_db()
    click.echo('Initialized the database.')


@click.command('clear-tables')
@with_appcontext
def clear_table_command():
    """Clear data from all the tables."""
    clear_tables()
    click.echo('Cleared all tables')


@click.command('clear-db')
@with_appcontext
def clear_db_command():
    """Drop all the tables"""
    clear_db()
    click.echo('Dropped all tables')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(clear_table_command)
    app.cli.add_command(clear_db_command)
