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

    q = QLearning.QLearning(160, 4)

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

    notsafe = [4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,\
     33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 58, 59, 68, 69, 70,\
     71, 72, 73, 74, 75, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,\
     101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 116, 117, 118, 119, 120, 121, 122, 123, 129, 130,\
     132, 133, 134, 135, 136, 137, 138, 139, 141, 142, 145, 146, 148, 149, 150, 151, 152, 153, 154, 155,\
     157,158]

    noreverse = [0, 1, 2, 3, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,81, 82, 83, 84, 85, 86,\
     87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,\
     110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 144, 145, 146,\
     147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159]

    while True:
        if not BrickPiUpdateValues():
            # pass
            curr_state = sumo.state()
            # curr_action = q.predict(curr_state) if 0.01 < random() else randint(0, 3)
            curr_action = q.predict(curr_state)
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
