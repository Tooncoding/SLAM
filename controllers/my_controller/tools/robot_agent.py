MAX_SPEED = 4

class RobotAgent:
    def __init__(self, robot, left_motor, right_motor):
        self.robot = robot
        self.timestep = int(robot.getBasicTimeStep())
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.max_speed = MAX_SPEED

    def execute(self, command):
        print("Executing command:", command)

        if command == "F":
            print("moving up")
            self.move_left()
        elif command == "B":
            print("moving down")
            self.move_right()
        elif command == "L":
            print("moving left")
            self.move_backward()  # ← you must implement this
        elif command == "R":
            print("moving right")
            self.move_forward()  # ← you must implement this
        elif command == "AVOID":
            print("avoiding")
            self.move_backward()
            self.counter_clockwise_spin()
            self.move_forward()
        else:
            print("⚠️ Unknown command:", command)
       
    def move_forward(self, coeff=1):
        # print("moving forward")
        count = 0
        while self.robot.step(self.timestep) != -1:
            if count > 29:
                break
            self.left_motor.setVelocity(coeff*self.max_speed)
            self.right_motor.setVelocity(coeff*self.max_speed)
            count += 1
        # print("stop")
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def move_backward(self, coeff=1):
        # print("moving backward")
        count = 0
        while self.robot.step(self.timestep) != -1:
            if count > 29:
                break
            self.left_motor.setVelocity(-coeff*self.max_speed)
            self.right_motor.setVelocity(-coeff*self.max_speed)
            count += 1
        print("stop")
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def counter_clockwise_spin(self, coeff=0.5):
        # print("CCW spin")
        count = 0
        while self.robot.step(self.timestep) != -1:
            if count > 32:
                break
            self.left_motor.setVelocity(-coeff*self.max_speed)
            self.right_motor.setVelocity(coeff*self.max_speed)
            count += 1
        # print("stop")
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def clockwise_spin(self, coeff=0.5):
        # print("CW spin")
        count = 0
        while self.robot.step(self.timestep) != -1:
            if count > 32:
                break
            self.left_motor.setVelocity(coeff*self.max_speed)
            self.right_motor.setVelocity(-coeff*self.max_speed)
            count += 1
        # print("stop")
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def move_left(self):
    # move left one tile worth of time
        self.counter_clockwise_spin()
        self.move_forward()
        self.clockwise_spin()

    def move_right(self):
        self.clockwise_spin()
        self.move_forward()
        self.counter_clockwise_spin()
