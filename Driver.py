from BrickPi import *
from threading import Thread
import time



class Driver(object):
    def __init__(self, MOTOR_PORT_L = PORT_C, MOTOR_PORT_R = PORT_B):

        BrickPiSetup()

        BrickPi.MotorEnable[MOTOR_PORT_L] = 1 #LEFT MOTOR
        BrickPi.MotorEnable[MOTOR_PORT_R] = 1 #RIGHT MOTOR

        self.LEFT_PORT = MOTOR_PORT_L
        self.RIGHT_PORT = MOTOR_PORT_R

        self.active = False

        self.BASE_SPEED = 0
        self.LEFT_SPEED = 0
        self.RIGHT_SPEED = 0

    def move(self, speed=20):
        self.active = True
        self.BASE_SPEED = speed

        self.LEFT_SPEED = self.BASE_SPEED
        self.RIGHT_SPEED = self.BASE_SPEED

        def move_thread():
            print 'Moving thread started'
            while self.active:
                BrickPi.MotorSpeed[self.LEFT_PORT] = self.LEFT_SPEED
                BrickPi.MotorSpeed[self.RIGHT_PORT] = self.RIGHT_SPEED
                # BrickPiUpdateValues()
                time.sleep(.2)
            #Loop end
            BrickPi.MotorSpeed[self.LEFT_PORT] = 0
            BrickPi.MotorSpeed[self.RIGHT_PORT] = 0

        #start the thread to move
        move_thread = Thread(target=move_thread, args=())
        move_thread.start()

    def speed(self, speed):
        self.BASE_SPEED = speed
        self.LEFT_SPEED = self.BASE_SPEED
        self.RIGHT_SPEED = self.BASE_SPEED
        BrickPi.MotorSpeed[self.LEFT_PORT] = self.LEFT_SPEED
        BrickPi.MotorSpeed[self.RIGHT_PORT] = self.RIGHT_SPEED

    def turn(self, delta = 0):
        '''
        delta > 0 -> turn right
        delta < 0 -> turn left
        '''
        delta = int(delta)
        self.LEFT_SPEED = self.BASE_SPEED + delta
        self.RIGHT_SPEED = self.BASE_SPEED - delta

        #set new speed
        BrickPi.MotorSpeed[self.LEFT_PORT] = self.LEFT_SPEED
        BrickPi.MotorSpeed[self.RIGHT_PORT] = self.RIGHT_SPEED

        #update speed
        BrickPiUpdateValues()

    def turn2(self, l, r):

        self.LEFT_SPEED = l
        self.RIGHT_SPEED = r

        #set new speed
        BrickPi.MotorSpeed[self.LEFT_PORT] = self.LEFT_SPEED
        BrickPi.MotorSpeed[self.RIGHT_PORT] = self.RIGHT_SPEED

        #update speed
        BrickPiUpdateValues()

    def turn3(self, p):

        self.LEFT_SPEED = int(p*self.BASE_SPEED)
        self.RIGHT_SPEED = -int(p*self.BASE_SPEED)

        #set new speed
        BrickPi.MotorSpeed[self.LEFT_PORT] = self.LEFT_SPEED
        BrickPi.MotorSpeed[self.RIGHT_PORT] = self.RIGHT_SPEED

        #update speed
        BrickPiUpdateValues()


    def straight(self):
        '''
        Turn the wheel straight
        '''
        self.LEFT_SPEED = self.BASE_SPEED
        self.RIGHT_SPEED = self.BASE_SPEED

        #set new speed
        BrickPi.MotorSpeed[self.LEFT_PORT] = self.LEFT_SPEED
        BrickPi.MotorSpeed[self.RIGHT_PORT] = self.RIGHT_SPEED

        #update speed
        BrickPiUpdateValues()

    def stop(self):
        self.active = False
        print "Motor Stoped"
        self.BASE_SPEED = 0
        self.LEFT_SPEED = self.BASE_SPEED
        self.RIGHT_SPEED = self.BASE_SPEED

def main():
    print "Starting"
    d = Driver(PORT_C, PORT_B)
    d.move()
    d.speed(20)
    time.sleep(3)
    d.speed(0)
    time.sleep(3)
    d.speed(30)
    time.sleep(3)
    d.stop()
    # #THREAD STUFF
    # t = Thread(target=d.move(), args=())
    # t.start()

    # time.sleep(1)
    # print "Turning"
    # #driver method
    # d.turn(0.5)
    # time.sleep(2)
    # d.stop()

if __name__ == '__main__':
    main()
