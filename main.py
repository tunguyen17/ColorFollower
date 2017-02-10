"""
Problem: Sumo sensor can't sense if object is too close, NEED 2 sumo sensor to cover the two tires
"""

from BrickPi import \
    PORT_C, PORT_B, \
    PORT_3, \
    BrickPiUpdateValues

import Driver
import Sumo

import time

def main():
    prez = Driver.Driver(PORT_C, PORT_B)
    print "Driver created"
    sumo = Sumo.Sumo(PORT_3)
    prez.move()
    prez.speed(50)
    print "prez moving"

    while True:
        if not BrickPiUpdateValues():
            if sumo.val()==1:
                prez.turn3(2)
                time.sleep(0.1)
            elif sumo.val()==2:
                prez.turn3(2)
                time.sleep(0.1)
            elif sumo.val()==3:
                prez.turn3(-2)
                time.sleep(0.1)
            else:
                prez.straight()


if __name__ == '__main__':
    main()
