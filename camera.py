import time
import threading
import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.latest_frame = None
        self.running = True

        # Start a single background thread to read frames from the USB camera
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        """Continuously reads frames in the background without blocking Flask."""
        while self.running:
            if not self.cap.isOpened():
                time.sleep(0.1)
                continue

            success, frame = self.cap.read()
            if success:
                # Encode once and store in memory
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    self.latest_frame = buffer.tobytes()

            # ~30 FPS pacing so we don't hog CPU
            time.sleep(0.03)

    def generate_frames(self):
        """Yields the latest frame from memory instantly."""
        while True:
            if self.latest_frame is not None:
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'
                    + self.latest_frame
                    + b'\r\n'
                )

            # Polite yield so Eventlet can process WASD keyboard presses
            time.sleep(0.03)

    def release(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()


# Global instance
_camera_instance = Camera(0)


def frames():
    return _camera_instance.generate_frames()