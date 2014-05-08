import struct
import time
import numpy
import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=.1)
N = 250
buffer = numpy.zeros((N, 3), numpy.byte)
def write():
    msg = (chr(0) * 2) + buffer.tostring()
    ser.write(msg)

def writeone(i):
    offset = struct.pack('H', 3 * i)
    msg = offset + buffer[i].tostring()
    ser.write(msg)

time.sleep(.1)
def setColor(r, g, b):
    buffer[:,0] = g
    buffer[:,1] = r
    buffer[:,2] = b

for i in range(1):
    setColor(25, 0, 0)
    write()
    time.sleep(1)
    setColor(0, 25, 0)
    write()
    time.sleep(1)

    setColor(0, 0, 25)
    write()
    time.sleep(1)

def sweep(color):
    for i in range(N):
        buffer[i] = color
        writeone(i)
        time.sleep(.01)
    print buffer[i]

while 1:
    for color in ([25, 0, 0], [0, 25, 0], [0, 0, 25]):
        sweep(color)
buffer *= 0
write()

