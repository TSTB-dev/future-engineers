
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
        self.straight_rotation=-10000#曲がってから次のturnゾーンに行くまでに青線を他の線を読まないようにする

        self.motor_steer = motor_steer
        self.motor = motor


    def straightening(self,throttle,bias):
        st_roll=self.motor.get()[0]

        #print("destination: ",self.destination)
        repair_yaw=hub.motion.yaw_pitch_roll()[0]


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


        return 0


    def change_steer(self,throttle,rot):
        blue_camera = (rot == 1)
        orange_camera = (rot == 2)
        xx=self.motor.get()[0]
        print("angle",xx)

        #terms_light_sensor = (h >  210-130) and ( h < 210+130) and(s > 256) and (s < 1024) and(v >= 0) and (v <= 1023)
        if xx-self.straight_rotation>=1400:
            if blue_camera:
                print("-------\n")
                print("blue get")

                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                while (this_angle-rel_pos)<=0:
                    self.straightening(throttle,0)
                    this_angle = self.motor.get()[0]

                hub.motion.yaw_pitch_roll(90+(hub.motion.yaw_pitch_roll()[0]))
                self.destination=0
                self.direction=-1
                self.straight_rotation=self.motor.get()[0]

            elif orange_camera:
                print("-------\n")
                print("orange get")
                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                while (this_angle-rel_pos)<=0:
                    self.straightening(throttle,0)
                    this_angle = self.motor.get()[0]

                hub.motion.yaw_pitch_roll(-90+(hub.motion.yaw_pitch_roll()[0]))
                self.destination=0
                self.direction=1
                self.straight_rotation=self.motor.get()[0]



    def back_turn(self,throttle,rot):
        check_line=False

        blue_camera = (rot == 1)
        orange_camera = (rot == 2)
        xx=self.motor.get()[0]
        print("angle",xx)
        #terms_light_sensor = (h >  210-130) and ( h < 210+130) and(s > 256) and (s < 1024) and(v >= 0) and (v <= 1023)
        if xx-self.straight_rotation>=1600:
            if blue_camera:
                print("-------\n")
                print("blue get_back")

                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                start=time.ticks_us()
                while (this_angle-rel_pos)<=1400:
                    self.straightening(throttle,0)
                    this_angle = self.motor.get()[0]
                    end=time.ticks_us()
                    if(end-start)/1000 >= 5000:
                        break

                hub.motion.yaw_pitch_roll(90+(hub.motion.yaw_pitch_roll()[0]))
                self.destination=0
                self.direction=-1

                d_steer= 4 * (hub.motion.yaw_pitch_roll()[0] - (self.destination)*self.direction)

                start=time.ticks_us()
                while abs(d_steer)>=40:
                    #print("--d_steer--",d_steer)
                    super().move(-0.8*throttle,d_steer)
                    d_steer= 4 * (hub.motion.yaw_pitch_roll()[0] - (self.destination)*self.direction)
                    if d_steer < -120:
                        d_steer = -120
                    elif d_steer > 120:
                        d_steer = 120
                    end=time.ticks_us()
                    #print("get angle time:{}[ms]".f
                    if(end-start)/1000 >= 4800:
                        break
                self.straight_rotation=self.motor.get()[0]
                check_line=True
            elif orange_camera:
                print("-------\n")
                print("orange get_back")

                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                start=time.ticks_us()
                while (this_angle-rel_pos)<=1400:
                    self.straightening(throttle,0)
                    this_angle = self.motor.get()[0]
                    end=time.ticks_us()
                    if(end-start)/1000 >= 5000:
                        break

                hub.motion.yaw_pitch_roll(-90+(hub.motion.yaw_pitch_roll()[0]))
                self.destination=0
                self.direction=1

                d_steer= 4 * (hub.motion.yaw_pitch_roll()[0] - (self.destination)*self.direction)

                start=time.ticks_us()
                while abs(d_steer)>=40:
                    #print("--d_steer--",d_steer)
                    super().move(-0.7*throttle,d_steer)

                    d_steer= 4 * (hub.motion.yaw_pitch_roll()[0] - (self.destination)*self.direction)
                    if d_steer < -120:
                        d_steer = -120
                    elif d_steer > 120:
                        d_steer = 120
                    end=time.ticks_us()
                    #print("get angle time:{}[ms]".f
                    if(end-start)/1000 >= 3000:
                        break
                self.straight_rotation=self.motor.get()[0]
                check_line=True


        return check_line
