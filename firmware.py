from BrickPi import *

I2C_PORT = PORT_1
I2C_ADDR = 0x02
I2C_DEVICE_INDEX = 0

BrickPiSetup()
BrickPi.SensorType[I2C_PORT] = TYPE_SENSOR_I2C

BrickPi.SensorI2CSpeed   [I2C_PORT]    = 0
BrickPi.SensorI2CDevices [I2C_PORT]    = 1

BrickPi.SensorI2CAddr    [I2C_PORT][I2C_DEVICE_INDEX] = I2C_ADDR


BrickPi.SensorSettings [I2C_PORT][I2C_DEVICE_INDEX]    = 0
BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_INDEX]    = 1
BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_INDEX]    = 8
BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_INDEX][0] = 0x00

if(BrickPiSetupSensors()):
  print "BrickPiSetupSensors failed for reading sensor firmware version."
  sys.exit( 0 )

if(BrickPiUpdateValues()):
  print "BrickPiUpdateValues failed for reading sensor firmware version."
  sys.exit(0)

if(BrickPi.Sensor[I2C_PORT] & (0x01 << I2C_DEVICE_INDEX)):
  dbytes = [ None ] * 8;
  for i in range(8):
    dbytes[i] = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_INDEX][i]
  firmwareVersion = ''.join( chr( x ) for x in dbytes )
  print "Firmware version  : ", firmwareVersion, " \t[", " ".join( hex( n ) for n in dbytes ), " ]"
