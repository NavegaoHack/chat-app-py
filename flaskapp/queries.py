from flaskapp.db import new_user, log_user, log_out, del_user, restore_passw, get_u_list, previous_messages, insert_new_message
from flask import Blueprint, request, Response
from json import dumps

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

@bp_auth.route('/get-users-list', methods=['GET'])
def get_user_list():
    user_list, status_code = get_u_list()

    return Response(dumps(user_list), status_code, mimetype='application/json')

@bp_auth.route('/get-previous-messages', methods=['GET'])
def get_previous_messages():
    #req = request.json
    #chat_id = req['chat-id']
    messages, status_code = previous_messages(1)
    
    return Response(dumps(messages), status_code, mimetype='application/json')

def store_message(author_id, message, chat_id):
    broadcast_response = insert_new_message(author_id, message, chat_id)

    return broadcast_response