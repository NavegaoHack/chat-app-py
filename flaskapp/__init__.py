import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

socket = SocketIO()

def create_app(test_config=None):
    #configuring the app
    app = Flask(__name__, instance_relative_config=True)
    # support cors for all domains
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.sqlite3'),
    )
    app.debug = True
    # ensuring that instance folder exists
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        print('instace path already exists')
        pass

    #setting the app for db functions ind db.py 
    from . import db
    db.set_app(app)

    #setting the app for db functions ind db.py 
    from . import queries
    app.register_blueprint(queries.bp_auth)

    @app.route('/')
    def index():
        return render_template('index.html')

    from . import sockets
    socket.init_app(app)
    return app