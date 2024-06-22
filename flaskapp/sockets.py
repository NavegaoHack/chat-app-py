from flask_socketio import emit
from . import socket


#handle message
@socket.on('chat-message')
def handle_chat_message(message):
    print(message)
    emit('broadcast-message', message, broadcast=True)