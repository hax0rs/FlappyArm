import pigpio
from time import sleep

pi = pigpio.pi()

servoPins = [4, 5, 6, 12, 13, 16, 17, 18]
servoPOI = [[500,1430,2360,1620],
            [500,1430,2360,2120],
            [720,1600,2390,1460],
            [700,1830,2500,2060],
            [500,1430,2400,1940],
            [550,1460,2440,1820],
            [530,1450,2450,1820],
            [820,1350,1710,1780]]

servoRest = [1430,1430,1300,880,1150,920,1980,910]

testPin = 6

while True:
    servoPin = servoPins[testPin]
    pi.set_servo_pulsewidth(servoPin, servoPOI[testPin][0])
    sleep(3)
    for i in range(servoPOI[testPin][0], servoPOI[testPin][2], 10):
        pi.set_servo_pulsewidth(servoPin, i)
        sleep(0.03)
    pi.set_servo_pulsewidth(servoPin, servoRest[testPin])
    sleep(3)

    while True:
        test = input("0, 1 or 2: ")
        print (servoPOI[testPin][int(test)])
        key = ""
        while key != "esc":
            pi.set_servo_pulsewidth(servoPin, servoPOI[testPin][int(test)])
            key = input(str(servoPOI[testPin][int(test)]) + ": ")
            if key == "w":
                servoPOI[testPin][int(test)] = servoPOI[testPin][int(test)] + 10
            else:
                servoPOI[testPin][int(test)] = servoPOI[testPin][int(test)] - 10
