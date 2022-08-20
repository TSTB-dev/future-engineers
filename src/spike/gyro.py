
from basic_motion import Basic_motion
import hub
import time
class Gyro(Basic_motion):
    def __init__(self, motor_steer,motor):
        super().__init__(motor_steer,motor)
        self.old_destination=0
        self.difference_steer=0
        #self.light_sensor=light_sensor
        self.direction=1
        self.destination=0
        self.straight_rotation=-10000#曲がってから次のturnゾーンに行くまでに青線を他の線を読まないようにする

        self.motor_steer = motor_steer
        self.motor = motor
        self.past_change=0  #0chnge 1back

        self.section_count = -1
        self.sign_count = 0
        self.turn=90
        #self.memory_sign = [[0,0],[0,0],[0,0],[0,0]]



    def straightening(self,throttle,bias):
        st_roll=self.motor.get()[0]

        #print("destination: ",self.destination)
        repair_yaw=hub.motion.yaw_pitch_roll()[0]

        if abs(repair_yaw)<=30:
            self.difference_steer = int(-4 * (repair_yaw + bias))
        else:
            self.difference_steer = int(-4 * (repair_yaw + bias))

        if self.difference_steer < -120:
            self.difference_steer = -120
        elif self.difference_steer > 120:
            self.difference_steer = 120

        super().move(throttle,self.difference_steer)


        return 0


    def change_steer(self,throttle,rot,go_angle,steer):
        check_line=False
        blue_camera = (rot == 1)
        orange_camera = (rot == 2)
        xx=self.motor.get()[0]

        #terms_light_sensor = (h >  210-130) and ( h < 210+130) and(s > 256) and (s < 1024) and(v >= 0) and (v <= 1023)
        if xx-self.straight_rotation>=2000:

            if blue_camera:
                self.section_count = self.section_count + 1
                rel_pos= self.motor.get()[0]
                this_angle=rel_pos

                while (this_angle-rel_pos)<go_angle:
                    self.straightening(throttle,0)
                    this_angle = self.motor.get()[0]

                print("-------\n")
                print("blue get")
                rel_pos= self.motor.get()[0]


                y=hub.motion.yaw_pitch_roll()[0]
                hub.motion.yaw_pitch_roll(self.turn+y)
                self.destination=0
                self.direction=-1
                self.straight_rotation=self.motor.get()[0]
                check_line=True
                self.past_change=0

            elif orange_camera:
                self.section_count = self.section_count + 1
                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                while (this_angle-rel_pos)<go_angle:
                    self.straightening(throttle,0)
                    this_angle = self.motor.get()[0]

                print("-------\n")
                print("orange get")

                rel_pos= self.motor.get()[0]

                y=hub.motion.yaw_pitch_roll()[0]
                hub.motion.yaw_pitch_roll(-1*self.turn+y)

                self.destination=0
                self.direction=1
                self.straight_rotation=self.motor.get()[0]
                check_line=True
                self.past_change=0

        return check_line









    def back_turn(self,throttle,rot,go_angle):
        check_line=False

        blue_camera = (rot == 1)
        orange_camera = (rot == 2)
        xx=self.motor.get()[0]
        #print("angle",xx)
        #terms_light_sensor = (h >  210-130) and ( h < 210+130) and(s > 256) and (s < 1024)
        if xx-self.straight_rotation>=2000:

            if blue_camera:
                print("-------\n")
                print("blue get_back")
                self.destination=0
                self.direction = -1

                self.section_count = self.section_count + 1
                self.sign_count = 0

                while hub.motion.yaw_pitch_roll()[0]<5:
                    super().move(40,100)
                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                start=time.ticks_us()
                while (this_angle-rel_pos)<go_angle:
                    #self.straightening(65,-20)
                    super().move(65,0)
                    this_angle = self.motor.get()[0]
                    end=time.ticks_us()
                    if(end-start)/1000 >= 3000:
                        break

                y=hub.motion.yaw_pitch_roll()[0]
                hub.motion.yaw_pitch_roll(self.turn+y)
                start=time.ticks_us()

                while hub.motion.yaw_pitch_roll()[0]>=20:
                    #print("--d_steer--",d_steer)
                    super().move(-70,120)
                    end=time.ticks_us()
                    if(end-start)/1000 >= 3000:
                        break
                rel_pos = self.motor.get()[0]
                while self.motor.get()[0]-rel_pos >= -300:
                    super().move(-70,0)
                    end=time.ticks_us()
                    if(end-start)/1000 >= 4000:
                        break
                self.straight_rotation=self.motor.get()[0]
                rel_pos = self.motor.get()[0]
                while self.motor.get()[0]-rel_pos <= 300:
                    super().move(50,10)
                check_line=True
                self.past_change=1

            elif orange_camera:
                print("-------\n")
                print("orange get_back")
                self.destination=0
                self.direction=1

                self.section_count = self.section_count + 1
                self.sign_count = 0

                while hub.motion.yaw_pitch_roll()[0]>-5:
                    super().move(40,-100)
                rel_pos= self.motor.get()[0]
                this_angle=rel_pos
                start=time.ticks_us()
                while (this_angle-rel_pos)<go_angle:
                    #self.straightening(65,20)
                    super().move(65,0)
                    this_angle = self.motor.get()[0]
                    end=time.ticks_us()
                    if(end-start)/1000 >= 3000:
                        break

                y=hub.motion.yaw_pitch_roll()[0]
                hub.motion.yaw_pitch_roll(-1*self.turn+y)

                start=time.ticks_us()

                while hub.motion.yaw_pitch_roll()[0]<=-20:
                    #print("--d_steer--",d_steer)
                    super().move(-70,-120)
                    end=time.ticks_us()
                    if(end-start)/1000 >= 3000:
                        break
                rel_pos = self.motor.get()[0]
                while self.motor.get()[0]-rel_pos >= -300:
                    super().move(-70,0)
                    end=time.ticks_us()
                    if(end-start)/1000 >= 4000:
                        break
                self.straight_rotation=self.motor.get()[0]
                rel_pos = self.motor.get()[0]
                while self.motor.get()[0]-rel_pos <= 300:
                    super().move(50,-10)
                check_line=True
                self.past_change=1


        return check_line



