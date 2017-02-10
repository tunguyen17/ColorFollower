"""
Problem: Sumo sensor can't sense if object is too close, NEED 2 sumo sensor to cover the two tires
"""

from BrickPi import \
    PORT_C, PORT_B, \
    PORT_1, PORT_3, \
    BrickPiUpdateValues, BrickPiSetupSensors

import Driver
import Sumo
import Pixy

import time

def main():
    pixy = Pixy.Pixy()
    #Focusing Pixy on just the first object
    pixy.setup_obj1()
    #sumo = Sumo.Sumo(PORT_3)

    #Setting up all sensor
    if(BrickPiSetupSensors()):
      print "BrickPiSetupSensors failed"
      sys.exit( 0 )




    prez = Driver.Driver(PORT_C, PORT_B)
    print "Driver created"

    prez.move()
    prez.speed(100)

    print "prez moving"
    while True:
        pos = pixy.center_pos()
        if pos:
            delta = pos[0]-75
            print delta
            prez.turn(1.5*delta)
        else:
            prez.turn3(0.7)
        time.sleep(0.02)


    # while True:
    #     if not BrickPiUpdateValues():
    #         if sumo.val()==1:
    #             prez.turn3(2)
    #             time.sleep(0.1)
    #         elif sumo.val()==2:
    #             prez.turn3(2)
    #             time.sleep(0.1)
    #         elif sumo.val()==3:
    #             prez.turn3(-2)
    #             time.sleep(0.1)
    #         else:
    #             prez.straight()


if __name__ == '__main__':
    main()
