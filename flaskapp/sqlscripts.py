from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid1
from flaskapp.db import get_db, close_db
import click

print(get_db, close_db)

def insertNewUser(username, password):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (str(uuid1()), username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        close_db()
        return f"User {username} is already registered.", 404

    close_db()
    return f"{userqname} has inserted correctly", 200

def insertNewChat(chat_id, user_id):
    db = get_db()
    chat_unique_id = str(uuid1())
    try:
        db.execute(
            "INSERT INTO chats VALUES (?, ?, ?)",
            (chat_unique_id, chat_id, user_id),
        )
        db.commit()
    except db.IntegrityError:
        close_db()
        return f"chat {chat_unique_id} cannot be saved", 404

    close_db()
    return f"chat {chat_unique_id} has inserted correctly", 200

#def getUserId()

@click.command('print-all-users')
def printAllUsers():
    db = get_db()
    allUsers = db.execute("SELECT username FROM users").fetchall()
    for user in allUsers:
        print(user["username"])

@click.command('create-def-users')
def createDefaultUsers():
    print(insertNewUser("A", "1234"))
    print(insertNewUser("B", "5678"))
    print(insertNewUser("C", "ABCD"))

def set_app(app):
    app.teardown_appcontext(close_db) # close db connection after return the response
    app.cli.add_command(createDefaultUsers) # add the new cli command
    app.cli.add_command(printAllUsers) # add the new cli command
