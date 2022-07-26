from basic_motion import Basic_motion
import hub
import time

class Gyro(Basic_motion):
    def __init__(self, motor_steer,motor,light_sensor):
        super().__init__(motor_steer,motor)
        self.old_destination=0
        self.difference_steer=0
        self.light_sensor=light_sensor
        self.direction=1
        self.destination=0
        self.straight_rotation=10000 #曲がってから次のturnゾーンに行くまでに青線を他の線を読まないようにする

        self.motor_steer = motor_steer
        self.motor = motor


    def straightening(self,throttle,bias):
        st_roll=self.motor.get()[0]
        repair_yaw = hub.motion.yaw_pitch_roll()[0]
        #print("destination: ",self.destination)


        self.difference_steer = int(
            -4 * (repair_yaw - (self.destination + bias)*self.direction)
        )  # steer's value difinition by hub.motion.position
        #print("before_yaw: ",hub.motion.yaw_pitch_roll()[0])
        #print("repair_yaw: ",repair_yaw)
        #print("dirrerencesteer: ",self.difference_steer/4)

        if self.difference_steer < -120:
            self.difference_steer = -120
        elif self.difference_steer > 120:
            self.difference_steer = 120

        super().move(throttle,self.difference_steer)
        en_roll=self.motor.get()[0]
        self.straight_rotation+=en_roll-st_roll
        return 0

    def change_steer(self):
        h = self.light_sensor.get(2)[0]
        s = self.light_sensor.get(2)[1]
        v = self.light_sensor.get(2)[2]
        #print("------------")
        #print("abs(difference_steer): ",abs(self.difference_steer))
        if(
        (abs(self.difference_steer)<=180) and #start up first
        (h >  210-30) and ( h < 210+30) and
        (s > 256) and (s < 1024) and
        (v >= 0) and (v <= 1023) ):  #if find blue(gabagaba)
            hub.motion.yaw_pitch_roll(90-(hub.motion.yaw_pitch_roll()[0]))
            self.destination=0
            self.direction=-1
            print("-------------")
            print("blue_line")
            print("-------------")

    def back_turn(self,throttle):
        h = self.light_sensor.get(2)[0]
        s = self.light_sensor.get(2)[1]
        v = self.light_sensor.get(2)[2]
        if(
        (self.straight_rotation>=720) and #start up first
        (h >  210-30) and ( h < 210+30) and
        (s > 256) and (s < 1024) and
        (v >= 0) and (v <= 1023) ):
            print("-------\n")
            print("blue get")

            rel_pos= self.motor.get()[0]
            this_angle=rel_pos
            while (this_angle-rel_pos)<=900:
                self.straightening(throttle,0)
                this_angle = self.motor.get()[0]

            hub.motion.yaw_pitch_roll(90+(hub.motion.yaw_pitch_roll()[0]))
            self.destination=0
            self.direction=-1

            d_steer= 4 * (hub.motion.yaw_pitch_roll()[0] - (self.destination)*self.direction)
            if d_steer < -120:
                d_steer = -120
            elif d_steer > 120:
                d_steer = 120

            while abs(d_steer)>=40:
                #print("--d_steer--",d_steer)
                super().move(-1*throttle,d_steer)
                #start=time.ticks_us()
                d_steer= 4 * (hub.motion.yaw_pitch_roll()[0] - (self.destination)*self.direction)
                #end=time.ticks_us()
                #print("get angle time:{}[ms]".format((end-start)/1000))
            self.straight_rotation=0
