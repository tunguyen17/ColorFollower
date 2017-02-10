from BrickPi import * #import BrickPi.py file to use BrickPi operations

#constant for directions (NEED UPDATES)
#1023 : 0
#429 : 1
#348 : 2
#660 # 3

LEFT = range(655, 665);
MIDDLE = range(343, 353);
RIGHT = range(425, 435);

class Sumo(object):
    #initializer
    def __init__(self, I2C_PORT = PORT_3):
        self.PORT = I2C_PORT #default value
        BrickPiSetup() #setup the serial port for communication
        BrickPi.SensorType[self.PORT] = TYPE_SENSOR_RAW #Set the type of sensor at port

    #Warning there can ony be 1 update value
    #class method
    def val(self):
        if not BrickPiUpdateValues(): #ask BrickPi to update values for sensors/motors
            sensor_value = BrickPi.Sensor[self.PORT]
            print sensor_value
            return 1 if sensor_value in LEFT \
              else 2 if sensor_value in MIDDLE\
              else 3 if sensor_value in RIGHT\
              else 0 #Nothing ahead
        else: #if the sensor does not response anything
            return 0

#main method
def main():
    s = Sumo(PORT_1)
    while True:
        if not BrickPiUpdateValues():
            print s.val()
            time.sleep(0.1)
if __name__ == "__main__":
    main()
