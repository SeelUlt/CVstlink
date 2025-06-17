import serial
import time
from threading import Event

BAUD_RATE = 115200

def removeComment(string):
    if (string.find(';') == -1):
        return string
    else: return string[:string.index(';')]

def removeEolChars(string):
    return string.strip()

def sendWakeUp(ser):
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)
    ser.flushInput()

def waitForMovement(ser, cleanedLine):

    Event().wait(1)

    if cleanedLine not in ['$X','$$']:
        idleCounter = 0
        while True:
            ser.reset_input_buffer()
            command = str.encode('?'+'\n')
            ser.write(command)
            grblOut = ser.readline()
            grblResponce = grblOut.strip().decode('utf-8')
            if grblResponce != 'ok':
                if grblResponce.find("Idle") > 0:
                    idleCounter += 1

            if idleCounter > 10:
                break
def streamCode(COM, gcode):
    with open(gcode, "r") as file, serial.Serial(COM, BAUD_RATE) as ser:
        sendWakeUp(ser)
        for line in file:
            cleanedLine = removeEolChars(removeComment(line))
            if cleanedLine:
                print ("sending code: " + str(cleanedLine))
                command = str.encode(line + "\n")
                ser.write(command)
                waitForMovement(ser, cleanedLine)
                grblOut = ser.readline()
                print(" : ", grblOut.strip().decode('utf-8'))
        print("sending gcode was succesful")
