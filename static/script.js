console.log("SCRIPT LOADED");

// Force WebSockets only, bypassing HTTP long-polling limits
const socket = io({
    transports: ["websocket"]
});

socket.on("connect", () => {
    console.log("CONNECTED TO SERVER! Socket ID:", socket.id);
});

socket.on("connect_error", (err) => {
    console.error("Socket Connection Error:", err);
});

// Capture keydown events
document.addEventListener("keydown", (event) => {
    console.log("KEY PRESSED:", event.key);
    
    socket.emit("control", {
        key: event.key
    });
});