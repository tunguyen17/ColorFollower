'''
PIXY spec:  640x400 50fps

#X 158 - Y 99
#X 319 - Y 199

# mid X = 75 +/- 5

'''

from BrickPi import *

class Pixy(object):
    def __init__(self, I2C_PORT = PORT_1):
        self.PORT = PORT_1
        I2C_ADDR = 0x02
        self.I2C_DEVICE_INDEX = 0

        BrickPiSetup()
        BrickPi.SensorType[self.PORT] = TYPE_SENSOR_I2C
        BrickPi.SensorI2CSpeed   [self.PORT]    = 0
        BrickPi.SensorI2CDevices [self.PORT]    = 1
        BrickPi.SensorI2CAddr    [self.PORT][self.I2C_DEVICE_INDEX] = I2C_ADDR


    def setup_obj1(self):
        BrickPi.SensorSettings [self.PORT][self.I2C_DEVICE_INDEX]    = 0
        BrickPi.SensorI2CWrite [self.PORT][self.I2C_DEVICE_INDEX]    = 1
        BrickPi.SensorI2CRead  [self.PORT][self.I2C_DEVICE_INDEX]    = 6
        BrickPi.SensorI2COut   [self.PORT][self.I2C_DEVICE_INDEX][0] = 0x42



    def val_raw(self):

        if(not BrickPiUpdateValues()):
            if(BrickPi.Sensor[self.PORT] & (0x01 << self.I2C_DEVICE_INDEX)):
                n_object = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][0]
                object_color = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][1]
                x_ul = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][2]
                y_ul = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][3]
                x_lr = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][4]
                y_lr = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][5]
                X = (x_ul + x_lr)/2
                Y = (y_ul + y_lr)/2
                if n_object > 0:
                    #print 'X: ', X, '- Y: ', Y, " Color: ", object_color
                    return BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][0:6]
        else:
            return None
    def center_pos(self):
        if(BrickPi.Sensor[self.PORT] & (0x01 << self.I2C_DEVICE_INDEX)):
            n_object = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][0]
            object_color = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][1]
            x_ul = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][2]
            y_ul = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][3]
            x_lr = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][4]
            y_lr = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][5]
            X = (x_ul + x_lr)/2
            Y = (y_ul + y_lr)/2
            if n_object > 0:
                return [X, Y]
            else:
                return None


def main():
    p = Pixy()
    p.setup_obj1()

    while True:
        pos = p.center_pos()
        if pos:
            print pos
        time.sleep(0.02)

if __name__ == '__main__':
    main()
