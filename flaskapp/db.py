import sqlite3
import click
from uuid import uuid1
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app, g, session


def check_fields(user, passw):
    return not (user and passw)
        


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

# USERS QUERIES

def new_user(username, password):
    if check_fields(username, password): 
        return f"all fields are needed",400
    
    db = get_db()

    try:
        db.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (str(uuid1()), username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return f"User {username} is already registered.", 404

    return f"{username} has inserted correctly", 200

def del_user():
    db = get_db()

    try:
        db.execute(
            "DELETE FROM users WHERE id = ?",(session['user_id'],),
        )
        db.commit()
    except db.IntegrityError:
        return f"An error has ocurred on deletion", 404

    username = session['username']
    session.clear()
    return f"{username} has deleted sucessfully", 200

def log_user(username, password):
    if check_fields(username, password): 
        return f"all fields are needed",400
    
    db = get_db()
 
    error = None
    user = db.execute(
        'select * from users where username = ?', (username,)
    ).fetchone()

    if user is None:
        return 'Incorrect username.', 404
    elif not check_password_hash(user['password'], password):
        return 'Incorrect password.', 404

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return f"{username} logged sucessfully",200

def restore_passw(user, newpassw):
    if not user: return f"a username are required", 401
    if not newpassw: return f"a new password are required, none data has changed", 401

    db = get_db()

    try:
        db.execute(
            "UPDATE users SET password = ? WHERE username = ?", (generate_password_hash(newpassw), user,)
        )
        db.commit()
    except db.IntegrityError:
        return f"An error has ocurred on updating", 404
    return f"{user} has updated sucessfully", 200


def log_out():
    username = session['username']
    session.clear()
    return f"{username} logout sucessfully",200


def get_u_list():
    db = get_db()
 
    query = db.execute(
        'SELECT id, username FROM users'
    ).fetchall()

    user_list = []
    for row in query:
        d = {
            "username": row['username'],
            "id": row['id'],
        }
        user_list.append(d)

    return user_list, 200

def previous_messages(id):
    db = get_db()
    print(id)
 
    query = db.execute(
        'SELECT username, message, created_at FROM messages INNER JOIN users ON users.id = messages.author_id WHERE chat_id = ? ORDER BY created_at', (id,)
    ).fetchall()

    message_list = []
    for row in query:
        d = {
            "username": row['username'],
            "message": row['message'],
            "created_at": row['created_at'].strftime("%Y/%m/%d, %H:%M:%S")
        }
        message_list.append(d)

    return message_list, 200

def select_last_message():
    db = get_db()

    query = db.execute(
        'SELECT username, message, created_at FROM messages INNER JOIN users ON users.id = messages.author_id ORDER BY created_at DESC LIMIT 1'
    ).fetchone()

    d = {
        "username": query['username'],
        "message": query['message'],
        "created_at": query['created_at'].strftime("%Y/%m/%d, %H:%M:%S")
    }

    return d


def insert_new_message(author_id, msg, chat_id):
    db = get_db()

    try:
        db.execute(
            "INSERT INTO messages(author_id, message, chat_id) VALUES (?, ?, ?)", (author_id, msg, chat_id)
        )
        db.commit()
    except db.IntegrityError:
        return None
    
    return select_last_message() 


# CHAT QUERIES


@click.command('initialize-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def set_app(app):
    app.teardown_appcontext(close_db) # close db connection after return the response
    app.cli.add_command(init_db_command) # add the new cli command