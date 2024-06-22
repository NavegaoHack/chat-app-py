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
        return f"User {username} is already registered.", 404

    return f"{username} has inserted correctly", 200

