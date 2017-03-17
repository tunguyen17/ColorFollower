"""
Problem: Sumo sensor can't sense if object is too close, NEED 2 sumo sensor to cover the two tires
"""

from BrickPi import \
    PORT_C, PORT_B, \
    PORT_1, PORT_3, \
    BrickPiUpdateValues, BrickPiSetupSensors

from random import uniform, randint, random



import Driver, Sumo2, Pixy, QLearning, sensors

import time

def main():

    pixy = Pixy.Pixy()
    #Focusing Pixy on just the first object
    pixy.setup_obj1()
    sumo = sensors.Sensors()

    q = QLearning.QLearning(64, 4)

    # state = {0 : 'track', 1 : 'avoid'}
    # prev_state = 'track'

    #Setting up all sensor
    if(BrickPiSetupSensors()):
      print "BrickPiSetupSensors failed"
      sys.exit( 0 )

    prez = Driver.Driver(PORT_C, PORT_B)
    print "Driver created"

    prez.move()
    prez.speed(130)
    # prez.speed(0)

    # print "prez moving"
    # while True:
    #
    #     if pos:

    #Initialize state
    prev_state = sumo.state()
    prev_action = 0

    action = {0 : lambda: prez.turn3(-0.8),\
              1 : lambda: prez.straight(),\
              2 : lambda: prez.back(),\
              3 : lambda: prez.turn3(0.8)}

    # action[0]()
    # reward = 0.1

    # good = [2, 66, 30, 94]
    #
    # found = [1, 3]
    #
    # safe = [28, 29, 31, 92, 93, 95,\
    #         12, 13, 14, 15, 76, 77, 78, 79,\
    #         16, 17, 18, 19, 80, 81, 82, 83,\
    #         0, 2, 3, 64, 65, 67\
    #         ]

    notsafe = [4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, \
    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

    noreverse = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26, 27, 29, 30, 31, 33, 34, \
    35, 37, 38, 39, 41, 42, 43, 45, 46, 47, 49, 50, 51, 53, 54, 55, 57, 58, 59, 61, 62, 63]

    while True:
        if not BrickPiUpdateValues():
            # pass
            curr_state = sumo.state()
            curr_action = q.predict(curr_state) if 0.0001 < random() else randint(0, 3)
            # curr_action = q.predict(curr_state)
            action[curr_action]()

            time.sleep(0.2)
            # BrickPiUpdateValues()
            # print 's : ', curr_state, '- a : ' ,curr_action, '- r :'

            # reward = 3 if (prev_state not in safe and curr_state in safe) else 10 if (curr_state in safe and curr_action == 1) else 0 if (curr_state in safe) else -3

            if curr_state in notsafe:
                reward = -5
            elif curr_state in noreverse and curr_action == -1:
                reward = -5
            elif curr_action == 1:
                reward = 10
                pos = pixy.center_pos()
                if pos:
                    delta = pos[0]-75
                    # print delta
                    prez.turn(0.5*delta)
                    reward = 50
            else:
                reward =-1

            print ''
            print 's : ', curr_state, '- a : ' ,curr_action, '- r : ', reward


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
                # pos = pixy.center_pos()
                # if pos:
                #     delta = pos[0]-75
                #     print delta
                #     prez.turn(0.5*delta)
                # else:
                #     prez.turn2(-50, 50)




if __name__ == '__main__':
    main()
