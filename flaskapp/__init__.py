import os
from flask import Flask, request,jsonify, render_template
from . import db
from . import sqlscripts
from flask_socketio import SocketIO, emit



#def create_app(test_config=None):
app = Flask(__name__, instance_relative_config=True)
socketio = SocketIO(app)
# ensuring that instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    print('instace path already exists')
    pass

@app.route('/')
def index_endpoint():
    return render_template("index.html")

@app.route('/send', methods=('POST',))
def parse_chats():
    data_received = request.get_json()
    print(data_received)
    data_to_send = {
        "title": "SUCCESSFULL :D",
        "body": "Message was sucessfully sended",
    }
    return jsonify(data_to_send)

# Socket IO



@socketio.on('connect')
def user_connected():
    print('user connnected')

@socketio.on('disconnect')
def user_disconnect():
    print('Client disconnected')

@socketio.on('message')
def receive_chat(message):
    print('message: ' + message)
    emit('response', {'message': message, 'other Person': 'other'}, broadcast=True)




#setting the app for db functions ind db.py 
db.set_app(app)
sqlscripts.set_app(app)

#return socketio, app

if __name__ == '__main__':
    socketio.run(app)
