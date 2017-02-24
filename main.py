"""
Problem: Sumo sensor can't sense if object is too close, NEED 2 sumo sensor to cover the two tires
"""

from BrickPi import \
    PORT_C, PORT_B, \
    PORT_1, PORT_3, \
    BrickPiUpdateValues, BrickPiSetupSensors

from random import uniform, randint, random



import Driver, Sumo2, Pixy, QLearning

import time

def main():

    pixy = Pixy.Pixy()
    #Focusing Pixy on just the first object
    pixy.setup_obj1()
    sumo = Sumo2.Sumo2()

    q = QLearning.QLearning(16, 4)

    # state = {0 : 'track', 1 : 'avoid'}
    # prev_state = 'track'

    #Setting up all sensor
    if(BrickPiSetupSensors()):
      print "BrickPiSetupSensors failed"
      sys.exit( 0 )

    prez = Driver.Driver(PORT_C, PORT_B)
    print "Driver created"

    prez.move()
    prez.speed(95)

    # print "prez moving"
    # while True:
    #
    #     if pos:

    #Initialize state
    prev_state = sumo.state()
    prev_action = 0

    action = {0 : lambda: prez.turn3(-1),\
              1 : lambda: prez.straight(),\
              2 : lambda: prez.back(),\
              3 : lambda: prez.turn3(1)}

    # action[0]()
    # reward = 0.1

    safe = [0, 3, 4, 7]

    while True:
        if not BrickPiUpdateValues():
            # pass
            curr_state = sumo.state()
            curr_action = q.predict(curr_state) if 0.01 < random() else randint(0, 3)

            action[curr_action]()

            time.sleep(0.2)
            # BrickPiUpdateValues()
            print 's : ', curr_state, '- a : ' ,curr_action

            # reward = 3 if (prev_state not in safe and curr_state in safe) else 10 if (curr_state in safe and curr_action == 1) else 0 if (curr_state in safe) else -3

            reward = 0 if (curr_state in safe) else -3

            print ''
            # print 's : ', curr_state, '- a : ' ,curr_action, '- r : ', reward

            q.train(prev_state, prev_action, curr_state, curr_action, reward)

            prev_state = curr_state
            prev_action = curr_action

            # time.sleep()
            # #obstacle ahead
            # obs = sumo.val()
            # if obs==1:
            #     prez.turn3(2)
            #     prev_state = 'avoid'
            # elif obs==2:
            #     prez.turn3(2)
            #     prev_state = 'avoid'
            # elif obs==3:
            #     prez.turn3(-2)
            #     prev_state = 'avoid'
            # else:
            #     #no obstacle find the color
            #     if prev_state == 'avoid':
            #         print "hello"
            #         prez.straight()
            #         prez.speed(prez.BASE_SPEED)
            #         BrickPiUpdateValues()
            #         # time.sleep(uniform(1, 5))
            #         time.sleep(3)
            #         prev_state = 'track'
            #         print "hello2"
            #     pos = pixy.center_pos()
            #     if pos:
            #         delta = pos[0]-75
            #         print delta
            #         prez.turn(0.5*delta)
            #     else:
            #         prez.turn2(-50, 50)




if __name__ == '__main__':
    main()
