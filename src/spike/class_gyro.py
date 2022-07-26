# ここにコードを書いてね :-)
class Gyro():
    def __init__(self, motor_steer,motor,light_sensor):
        super().__init__(motor_steer,motor)
        self.destination=0
        self.differece_steer=0
        self.light_sensor=light_sensor


    def straightening(self,throttle,bias):

        while True:
            self.difference_steer = int(
                -4 * ((self.destination + bias)%360 - hub.motion.yaw_pitch_roll()[0])
            )  # steer's value difinition by hub.motion.position
            if self.difference_steer < -110:
                self.difference_steer = -110
            elif self.difference_steer > 110:
                self.difference_steer = 110

            move(throttle,self.difference_steer)

            if motor_steer.get(2)[0] == 0:
                motor_steer.run_to_position(0)
                motor_steer.brake

        return 0;

    def change_steer(self):
        while True:
            if(
            (abs(self.differece_steer)<=10) and #start up first
            (light_sensor.get(2)[0] > 0) and (light_sensor.get(2)[0] < 400) and
            (light_sensor.get(2)[1] > 100) and (light_sensor.get(2)[1] < 500) and
            (light_sensor.get(2)[2] > 300) and (light_sensor.get(2)[2] < 700) and
            (light_sensor.get(2)[3] > 400) and (light_sensor.get(2)[3] < 800)  ):  #if find blue(gabagaba)
                self.destination+=90



