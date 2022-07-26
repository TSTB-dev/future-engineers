from basic_motion import Basic_motion
import hub
class Avoid_color_sign(Basic_motion):
    avoid_angle = 120
    speed = 20
    bias = 0
    def __init__(self,motor_steer,motor):
        super().__init__(motor_steer,motor)

    def avoidRed(self):
        super().move(self.speed,self.avoid_angle)
        self.bias = -20

    def avoidGreen(self):
        super().move(self.speed,-self.avoid_angle)
        self.bias = 20

    def setBias(self,new_bias):
        self.bias = new_bias

    def getBias(self):
        return self.bias
