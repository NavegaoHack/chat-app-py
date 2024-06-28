from flask_socketio import emit
from . import socket
from .queries import store_message


#handle message
@socket.on('chat-message')
def handle_chat_message(listen):

    response = store_message(listen['userId'], listen['message'], 1)

    emit('broadcast-message', response, broadcast=True)

@socket.on('connected-user')
def notify_connected_chat(class_element):
    print(class_element)
    emit('broadcast-connected-user', class_element, broadcast=True)