from BrickPi import *

I2C_PORT = PORT_1
I2C_ADDR = 0x02
I2C_DEVICE_INDEX = 0

I2C_REG = 0x43

BrickPiSetup()
BrickPi.SensorType[I2C_PORT] = TYPE_SENSOR_I2C
BrickPi.SensorI2CSpeed   [I2C_PORT]    = 0
BrickPi.SensorI2CDevices [I2C_PORT]    = 1
BrickPi.SensorI2CAddr    [I2C_PORT][I2C_DEVICE_INDEX] = I2C_ADDR


BrickPi.SensorSettings [I2C_PORT][I2C_DEVICE_INDEX]    = 0
BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_INDEX]    = 1
BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_INDEX]    = 6
BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_INDEX][0] = 0x42

if(BrickPiSetupSensors()):
  print "BrickPiSetupSensors failed"
  sys.exit( 0 )

while True:
    if(not BrickPiUpdateValues()):
        if(BrickPi.Sensor[I2C_PORT] & (0x01 << I2C_DEVICE_INDEX)):
            print BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_INDEX][0:4]
