import hub
class Basic_motion:
    def __init__(self,motor_steer,motor):
        self.motor_steer = motor_steer
        self.motor = motor

    def move(self,throttle, steer):
        self.motor.run_at_speed(throttle)
        once = False
        count = 0
        if steer > 120:
            steer = 120
        elif steer < -120:
            steer = -120

        while True:

            if(self.motor_steer.busy(type=1)): #if motor_steer is moving
                #print("motor_steer:",self.motor_steer.get(2)[0])
                count = count + 1
                continue
            elif once:
                break
            else:
                self.motor_steer.run_to_position(steer)
                once = True

    def stop(self):
        self.motor.brake()
        self.motor_steer.brake()
