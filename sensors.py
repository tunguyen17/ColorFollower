from BrickPi import * #import BrickPi.py file to use BrickPi operations
import Pixy
import firmware

#constant for directions (NEED UPDATES)
#1023
#656
#344
#424

#1023
#656
#344
#425

LEFT = range(650, 670);
MIDDLE = range(340, 360);
RIGHT = range(420, 440);

class Sensors(object):
    #initializer
    def __init__(self, I2C_PORT_PIXY = PORT_1, I2C_PORT_BACK = PORT_2, I2C_PORT_LEFT = PORT_3, I2C_PORT_RIGHT = PORT_4):

        self.states = {\
            '0-0-0':0, '0-0-1':1, '0-0-2':2, '0-0-3':3, '0-1-0':4, '0-1-1':5, '0-1-2':6,\
            '0-1-3':7, '0-2-0':8, '0-2-1':9, '0-2-2':10, '0-2-3':11, '0-3-0':12, '0-3-1':13,\
            '0-3-2':14, '0-3-3':15, '1-0-0':16, '1-0-1':17, '1-0-2':18, '1-0-3':19, '1-1-0':20,\
            '1-1-1':21, '1-1-2':22, '1-1-3':23, '1-2-0':24, '1-2-1':25, '1-2-2':26, '1-2-3':27,\
            '1-3-0':28, '1-3-1':29, '1-3-2':30, '1-3-3':31, '2-0-0':32, '2-0-1':33, '2-0-2':34,\
            '2-0-3':35, '2-1-0':36, '2-1-1':37, '2-1-2':38, '2-1-3':39, '2-2-0':40, '2-2-1':41,\
            '2-2-2':42, '2-2-3':43, '2-3-0':44, '2-3-1':45, '2-3-2':46, '2-3-3':47, '3-0-0':48,\
            '3-0-1':49, '3-0-2':50, '3-0-3':51, '3-1-0':52, '3-1-1':53, '3-1-2':54, '3-1-3':55,\
            '3-2-0':56, '3-2-1':57, '3-2-2':58, '3-2-3':59, '3-3-0':60, '3-3-1':61, '3-3-2':62,\
            '3-3-3':63\
            }

        # SUMO SENSOR
        self.PORT_BACK = I2C_PORT_BACK
        self.PORT_LEFT = I2C_PORT_LEFT
        self.PORT_RIGHT = I2C_PORT_RIGHT
        BrickPiSetup() #setup the serial port for communication

        BrickPi.SensorType[self.PORT_BACK] = TYPE_SENSOR_RAW
        BrickPi.SensorType[self.PORT_LEFT] = TYPE_SENSOR_RAW
        BrickPi.SensorType[self.PORT_RIGHT] = TYPE_SENSOR_RAW

        # PIXY SENSOR

        self.PORT_PIXY = PORT_1
        I2C_ADDR = 0x02

        BrickPiSetup()
        BrickPi.SensorType[self.PORT_PIXY] = TYPE_SENSOR_I2C
        BrickPi.SensorI2CSpeed   [self.PORT_PIXY]    = 0
        BrickPi.SensorI2CDevices [self.PORT_PIXY]    = 1
        BrickPi.SensorI2CAddr    [self.PORT_PIXY][0] = I2C_ADDR

        # SETUP TO READ COLOR
        BrickPi.SensorSettings [self.PORT_PIXY][0]    = 0
        BrickPi.SensorI2CWrite [self.PORT_PIXY][0]    = 1
        BrickPi.SensorI2CRead  [self.PORT_PIXY][0]    = 6
        BrickPi.SensorI2COut   [self.PORT_PIXY][0][0] = 0x42

    #Warning there can ony be 1 update value
    #class method
    def val_left(self):
        sensor_value = BrickPi.Sensor[self.PORT_LEFT]
        #print sensor_value
        return 1 if sensor_value in LEFT \
          else 2 if sensor_value in MIDDLE\
          else 3 if sensor_value in RIGHT\
          else 0 #Nothing ahead

    def val_right(self):
        sensor_value = BrickPi.Sensor[self.PORT_RIGHT]
        #print sensor_value
        return 1 if sensor_value in LEFT \
          else 2 if sensor_value in MIDDLE\
          else 3 if sensor_value in RIGHT\
          else 0 #Nothing ahead

    def val_back(self):
        sensor_value = BrickPi.Sensor[self.PORT_BACK]
        #print sensor_value
        # print sensor_value
        return 1 if (sensor_value in LEFT or sensor_value in MIDDLE or sensor_value in RIGHT) else 0 #Nothing ahead

    def center_pos(self):
        if(BrickPi.Sensor[self.PORT_PIXY] & (0x01 << 0)):
            n_object = BrickPi.SensorI2CIn[self.PORT_PIXY][0][0]
            x_ul = BrickPi.SensorI2CIn[self.PORT_PIXY][0][2]
            x_lr = BrickPi.SensorI2CIn[self.PORT_PIXY][0][4]
            X = (x_ul + x_lr)/2

            pos = 0

            if n_object > 0:
                # print 'RAW - ', X
                # print ''

                if X > 80:
                    pos = 3
                elif X >= 60:
                    pos = 2
                else:
                    pos = 1
            # print 'X - ', X, ' - Pos - ', pos
            return pos

    def state(self):
        # print self.val_back()
        # print  self.center_pos()
        # BACK - LEFT - RIGHT - CENTER
        # return '{}-{}-{}-{}'.format(self.val_back(), self.val_left(), self.val_right(), self.center_pos())
        return self.states['{}-{}-{}'.format(self.val_back(), self.val_left(), self.val_right())]


#main method
def main():
    s = Sensors()
    while True:
        if not BrickPiUpdateValues():
            val = s.state()
            print val
            # print ''
            time.sleep(0.02)
if __name__ == "__main__":
    main()
