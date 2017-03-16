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
            '0-0-0-0' : 0, '0-0-0-1' : 1, '0-0-0-2' : 2, '0-0-0-3' : 3, '0-0-1-0' : 4, '0-0-1-1' : 5, \
            '0-0-1-2' : 6, '0-0-1-3' : 7, '0-0-2-0' : 8, '0-0-2-1' : 9, '0-0-2-2' : 10, '0-0-2-3' : 11, \
            '0-0-3-0' : 12, '0-0-3-1' : 13, '0-0-3-2' : 14, '0-0-3-3' : 15, '0-1-0-0' : 16, '0-1-0-1' : 17,\
            '0-1-0-2' : 18, '0-1-0-3' : 19, '0-1-1-0' : 20, '0-1-1-1' : 21, '0-1-1-2' : 22, '0-1-1-3' : 23,\
            '0-1-2-0' : 24, '0-1-2-1' : 25, '0-1-2-2' : 26, '0-1-2-3' : 27, '0-1-3-0' : 28, '0-1-3-1' : 29,\
            '0-1-3-2' : 30, '0-1-3-3' : 31, '0-2-0-0' : 32, '0-2-0-1' : 33, '0-2-0-2' : 34, '0-2-0-3' : 35,\
            '0-2-1-0' : 36, '0-2-1-1' : 37, '0-2-1-2' : 38, '0-2-1-3' : 39, '0-2-2-0' : 40, '0-2-2-1' : 41,\
            '0-2-2-2' : 42, '0-2-2-3' : 43, '0-2-3-0' : 44, '0-2-3-1' : 45, '0-2-3-2' : 46, '0-2-3-3' : 47,\
            '0-3-0-0' : 48, '0-3-0-1' : 49, '0-3-0-2' : 50, '0-3-0-3' : 51, '0-3-1-0' : 52, '0-3-1-1' : 53,\
            '0-3-1-2' : 54, '0-3-1-3' : 55, '0-3-2-0' : 56, '0-3-2-1' : 57, '0-3-2-2' : 58, '0-3-2-3' : 59,\
            '0-3-3-0' : 60, '0-3-3-1' : 61, '0-3-3-2' : 62, '0-3-3-3' : 63, '1-0-0-0' : 64, '1-0-0-1' : 65,\
            '1-0-0-2' : 66, '1-0-0-3' : 67, '1-0-1-0' : 68, '1-0-1-1' : 69, '1-0-1-2' : 70, '1-0-1-3' : 71,\
            '1-0-2-0' : 72, '1-0-2-1' : 73, '1-0-2-2' : 74, '1-0-2-3' : 75, '1-0-3-0' : 76, '1-0-3-1' : 77,\
            '1-0-3-2' : 78, '1-0-3-3' : 79, '1-1-0-0' : 80, '1-1-0-1' : 81, '1-1-0-2' : 82, '1-1-0-3' : 83,\
            '1-1-1-0' : 84, '1-1-1-1' : 85, '1-1-1-2' : 86, '1-1-1-3' : 87, '1-1-2-0' : 88, '1-1-2-1' : 89,\
            '1-1-2-2' : 90, '1-1-2-3' : 91, '1-1-3-0' : 92, '1-1-3-1' : 93, '1-1-3-2' : 94, '1-1-3-3' : 95,\
            '1-2-0-0' : 96, '1-2-0-1' : 97, '1-2-0-2' : 98, '1-2-0-3' : 99, '1-2-1-0' : 100, '1-2-1-1' : 101,\
            '1-2-1-2' : 102, '1-2-1-3' : 103, '1-2-2-0' : 104, '1-2-2-1' : 105, '1-2-2-2' : 106,\
            '1-2-2-3' : 107, '1-2-3-0' : 108, '1-2-3-1' : 109, '1-2-3-2' : 110, '1-2-3-3' : 111,\
            '1-3-0-0' : 112, '1-3-0-1' : 113, '1-3-0-2' : 114, '1-3-0-3' : 115, '1-3-1-0' : 116,\
            '1-3-1-1' : 117, '1-3-1-2' : 118, '1-3-1-3' : 119, '1-3-2-0' : 120, '1-3-2-1' : 121,\
            '1-3-2-2' : 122, '1-3-2-3' : 123, '1-3-3-0' : 124, '1-3-3-1' : 125, '1-3-3-2' : 126,\
            '1-3-3-3' : 127, '0-0-0-None' : 128,'0-0-1-None' : 129,'0-0-2-None' : 130,\
            '0-0-3-None' : 131,'0-1-0-None' : 132,'0-1-1-None' : 133,'0-1-2-None' : 134,\
            '0-1-3-None' : 135,'0-2-0-None' : 136,'0-2-1-None' : 137,'0-2-2-None' : 138,\
            '0-2-3-None' : 139,'0-3-0-None' : 140,'0-3-1-None' : 141,'0-3-2-None' : 142,\
            '0-3-3-None' : 143,'1-0-0-None' : 144,'1-0-1-None' : 145,'1-0-2-None' : 146,\
            '1-0-3-None' : 147,'1-1-0-None' : 148,'1-1-1-None' : 149,'1-1-2-None' : 150,\
            '1-1-3-None' : 151,'1-2-0-None' : 152,'1-2-1-None' : 153,'1-2-2-None' : 154,\
            '1-2-3-None' : 155,'1-3-0-None' : 156,'1-3-1-None' : 157,'1-3-2-None' : 158,\
            '1-3-3-None' : 159
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
        return self.states['{}-{}-{}-{}'.format(self.val_back(), self.val_left(), self.val_right(), self.center_pos())]


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
