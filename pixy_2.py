'''
PIXY spec:  640x400 50fps
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

    def val(self):
        BrickPi.SensorSettings [self.PORT][self.I2C_DEVICE_INDEX]    = 0
        BrickPi.SensorI2CWrite [self.PORT][self.I2C_DEVICE_INDEX]    = 1
        BrickPi.SensorI2CRead  [self.PORT][self.I2C_DEVICE_INDEX]    = 6
        BrickPi.SensorI2COut   [self.PORT][self.I2C_DEVICE_INDEX][0] = 0x42

        if(BrickPiSetupSensors()):
          print "BrickPiSetupSensors failed"
          sys.exit( 0 )

        while True:
            if(not BrickPiUpdateValues()):
                if(BrickPi.Sensor[self.PORT] & (0x01 << self.I2C_DEVICE_INDEX)):
                    n_object = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][0]
                    object_color = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][4]
                    x_ul = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][1]
                    y_ul = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][2]
                    x_lr = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][3]
                    y_lr = BrickPi.SensorI2CIn[self.PORT][self.I2C_DEVICE_INDEX][4]

                    X = (x_ul + x_lr)/2
                    Y = (y_ul + y_lr)/2

                    if n_object > 0:
                        print 'X: ', X, '- Y: ', Y, " Color: ", object_color
            time.sleep(0.02)

def main():
    p = Pixy()
    p.val()

if __name__ == '__main__':
    main()
