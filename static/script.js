const socket = io();

const keys = {
    w: false,
    a: false,
    s: false,
    d: false
};


function sendCommand(key, pressed) {

    socket.emit("command", {
        key: key,
        pressed: pressed
    });

}


function stopRobot() {

    keys.w = false;
    keys.a = false;
    keys.s = false;
    keys.d = false;

    document.querySelectorAll(".key").forEach(
        function(element) {
            element.classList.remove("active");
        }
    );

    socket.emit("stop");

    document.getElementById("status").innerText =
        "STOPPED";
}


document.addEventListener(
    "keydown",
    function(event) {

        const key = event.key.toLowerCase();

        if (!keys.hasOwnProperty(key)) {
            return;
        }

        event.preventDefault();

        // Ignore browser auto-repeat
        if (keys[key]) {
            return;
        }

        keys[key] = true;

        document
            .getElementById(key)
            .classList.add("active");

        document.getElementById("status").innerText =
            "MOVING: " + key.toUpperCase();

        sendCommand(key, true);
    }
);


document.addEventListener(
    "keyup",
    function(event) {

        const key = event.key.toLowerCase();

        if (!keys.hasOwnProperty(key)) {
            return;
        }

        event.preventDefault();

        keys[key] = false;

        document
            .getElementById(key)
            .classList.remove("active");

        sendCommand(key, false);

        // If no keys are being held, make absolutely
        // sure the motors stop.
        if (
            !keys.w &&
            !keys.a &&
            !keys.s &&
            !keys.d
        ) {

            socket.emit("stop");

            document.getElementById("status").innerText =
                "STOPPED";
        }

    }
);


window.addEventListener(
    "blur",
    function() {

        stopRobot();

    }
);

document.addEventListener(
    "visibilitychange",
    function() {

        if (document.hidden) {
            stopRobot();
        }

    }
);


socket.on(
    "disconnect",
    function() {

        stopRobot();

        document.getElementById("status").innerText =
            "CONNECTION LOST - STOPPED";
    }
);
