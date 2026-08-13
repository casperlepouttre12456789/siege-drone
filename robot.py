import pigpio
import time
LEFT_SERVO = 12
RIGHT_SERVO = 13
LEFT_STOP = 1500
RIGHT_STOP = 1500
SPEED = 250
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Could not connect to pigpio")

def set_servos(left, right):
    left = max(1000, min(2000, left))
    right = max(1000, min(2000, right))

    pi.set_servo_pulsewidth(LEFT_SERVO, left)
    pi.set_servo_pulsewidth(RIGHT_SERVO, right)

def stop():
    set_servos(LEFT_STOP, RIGHT_STOP)

def forward():
    set_servos(
        LEFT_STOP + SPEED,
        RIGHT_STOP - SPEED
    )

def backward():
    set_servos(
        LEFT_STOP - SPEED,
        RIGHT_STOP + SPEED
    )

def left_turn():
    set_servos(
        LEFT_STOP - SPEED,
        RIGHT_STOP - SPEED
    )

def right_turn():
    set_servos(
        LEFT_STOP + SPEED,
        RIGHT_STOP + SPEED
    )

def cleanup():
    stop()
    time.sleep(0.2)
    pi.stop()
