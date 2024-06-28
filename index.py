from flaskapp import create_app, socket

app = create_app()

if __name__ == "__main__":
    socket.run(app, "0.0.0.0")