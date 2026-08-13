from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import robot
import cv2
import time
import threading

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

camera = cv2.VideoCapture(0)

last_command = time.time()

COMMAND_TIMEOUT = 0.5


@app.route("/")
def index():
    return render_template("index.html")


def camera_stream():
    while True:

        success, frame = camera.read()

        if not success:
            continue

        frame = cv2.resize(frame, (640, 480))

        success, jpeg = cv2.imencode(
            ".jpg",
            frame
        )

        if not success:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + jpeg.tobytes()
            + b"\r\n"
        )

        time.sleep(0.03)


@app.route("/camera")
def camera_feed():
    return Response(
        camera_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@socketio.on("command")
def command(data):

    global last_command

    last_command = time.time()

    key = data.get("key")
    pressed = data.get("pressed")

    if not pressed:
        robot.stop()
        return

    if key == "w":
        robot.forward()

    elif key == "s":
        robot.backward()

    elif key == "a":
        robot.left_turn()

    elif key == "d":
        robot.right_turn()

    else:
        robot.stop()


@socketio.on("stop")
def emergency_stop():

    global last_command

    last_command = time.time()

    robot.stop()


def watchdog():

    global last_command

    while True:

        time.sleep(0.1)

        if time.time() - last_command > COMMAND_TIMEOUT:
            robot.stop()


watchdog_thread = threading.Thread(
    target=watchdog,
    daemon=True
)

watchdog_thread.start()
if __name__ == "__main__":

    try:

        print("================================")
        print("       RECON DRONE")
        print("================================")
        print()
        print("Left servo : GPIO12 / Pin 32")
        print("Right servo: GPIO13 / Pin 33")
        print("Camera     : USB")
        print()
        print("Starting web server...")
        print()

        socketio.run(
            app,
            host="0.0.0.0",
            port=5000,
            allow_unsafe_werkzeug=True
        )

    except KeyboardInterrupt:
        pass

    finally:

        robot.cleanup()
        camera.release()
