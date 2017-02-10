"""
Problem: Sumo sensor can't sense if object is too close, NEED 2 sumo sensor to cover the two tires
"""

from BrickPi import \
    PORT_C, PORT_B, \
    PORT_1, PORT_3, \
    BrickPiUpdateValues, BrickPiSetupSensors

from random import uniform

import Driver
import Sumo
import Pixy

import time

def main():
    pixy = Pixy.Pixy()
    #Focusing Pixy on just the first object
    pixy.setup_obj1()
    sumo = Sumo.Sumo(PORT_3)

    state = {0 : 'track', 1 : 'avoid'}
    prev_state = 'track'

    #Setting up all sensor
    if(BrickPiSetupSensors()):
      print "BrickPiSetupSensors failed"
      sys.exit( 0 )




    prez = Driver.Driver(PORT_C, PORT_B)
    print "Driver created"

    prez.move()
    prez.speed(50)

    # print "prez moving"
    # while True:
    #
    #     if pos:


    while True:
        if not BrickPiUpdateValues():

            #obstacle ahead
            obs = sumo.val()
            if obs==1:
                prez.turn3(2)
                prev_state = 'avoid'
            elif obs==2:
                prez.turn3(2)
                prev_state = 'avoid'
            elif obs==3:
                prez.turn3(-2)
                prev_state = 'avoid'
            else:
                #no obstacle find the color
                if prev_state == 'avoid':
                    print "hello"
                    prez.straight()
                    prez.speed(prez.BASE_SPEED)
                    BrickPiUpdateValues()
                    # time.sleep(uniform(1, 5))
                    time.sleep(3)
                    prev_state = 'track'
                    print "hello2"
                pos = pixy.center_pos()
                if pos:
                    delta = pos[0]-75
                    print delta
                    prez.turn(0.5*delta)
                else:
                    prez.turn2(-50, 50)

            time.sleep(0.2)



if __name__ == '__main__':
    main()
