from flaskapp.db import new_user, log_user, log_out, del_user, restore_passw
from flask import Blueprint, request, Response

bp_auth = Blueprint('auth', __name__, url_prefix='/api/users')

@bp_auth.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message, status_code = new_user(username, password)

        return Response(message, status_code)
    
@bp_auth.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        username = request.form['username']
        password = request.form['password']
        message, status_code = log_user(username, password)

        return Response(message, status_code)

@bp_auth.route('/logout', methods=['GET', 'POST'])
def logout_user():
    if request.method == 'GET':
        message, status_code = log_out()
        
        return Response(message, status_code)

@bp_auth.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'GET':
        message, status_code = del_user()
        
        return Response(message, status_code)

@bp_auth.route('/update-passw', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new-password']
        message, status_code = restore_passw(username, new_password)
        
        return Response(message, status_code)


bp_messages = Blueprint('messages', __name__, url_prefix='/api/messages')

@bp_messages.route('/get-previous-messages', methods=['GET'])
def register_message():
    #messages, status_code = get_prev_messages()
    pass
        