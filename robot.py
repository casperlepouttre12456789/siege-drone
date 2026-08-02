class Robot:


    def move(self, command):

        if command["forward"]:
            print("Drive forward")

        elif command["backward"]:
            print("Drive backward")

        elif command["left"]:
            print("Turn left")

        elif command["right"]:
            print("Turn right")

        else:
            print("Drive stop")


    def camera(self, command):

        if command["camera_up"]:
            print("Camera tilt up")

        elif command["camera_down"]:
            print("Camera tilt down")

        else:
            print("Camera stop")


robot = Robot()
