from BrickPi import * #import BrickPi.py file to use BrickPi operations

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

class Sumo2(object):
    #initializer
    def __init__(self, I2C_PORT_LEFT = PORT_3, I2C_PORT_RIGHT = PORT_4):

        self.states = {\
                       '0-0' : 0 , '0-4' : 1 , '0-5' : 3 , '0-6' : 3, \
                       '1-0' : 4 , '1-4' : 5 , '1-5' : 6 , '1-6' : 7, \
                       '2-0' : 8 , '2-4' : 9 , '2-5' : 10, '2-6' : 11, \
                       '3-0' : 12, '3-4' : 13, '3-5' : 14, '3-6' : 15, \
                      }

        self.PORT_LEFT = I2C_PORT_LEFT
        self.PORT_RIGHT = I2C_PORT_RIGHT

        BrickPiSetup() #setup the serial port for communication

        BrickPi.SensorType[self.PORT_LEFT] = TYPE_SENSOR_RAW
        BrickPi.SensorType[self.PORT_RIGHT] = TYPE_SENSOR_RAW

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
        return 4 if sensor_value in LEFT \
          else 5 if sensor_value in MIDDLE\
          else 6 if sensor_value in RIGHT\
          else 0 #Nothing ahead

    def state(self):
        return self.states['{}-{}'.format(self.val_left(), self.val_right())]


#main method
def main():
    s = Sumo2()
    while True:
        if not BrickPiUpdateValues():
            print s.state()
            print ''
            time.sleep(0.5)
if __name__ == "__main__":
    main()
