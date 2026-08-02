import eventlet
eventlet.monkey_patch()  # Must be line 1 and 2!

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from camera import frames

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    logger=True,
    engineio_logger=True
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(
        frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@socketio.on("connect")
def connected():
    print(">>> CLIENT CONNECTED <<<")


@socketio.on("disconnect")
def disconnected():
    print(">>> CLIENT DISCONNECTED <<<")


@socketio.on("control")
def control(data):
    print(">>> COMMAND RECEIVED:", data)


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False
    )