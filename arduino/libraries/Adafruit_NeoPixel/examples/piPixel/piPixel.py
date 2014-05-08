from numpy import arange
import struct
import time
import numpy
import serial

A5 = 19

def Color(r, g, b):
    return numpy.array([g, r, b])

class NeoPixel:
    def __init__(self, N, port, pin):
        self.ser = serial.Serial(port, baudrate=115200, timeout=.1)
        self.N = N
        self.buffer = numpy.zeros((8, N, 3), numpy.byte)
        # TODO: record pin

    def show(self):
        for col, row in enumerate(self.buffer):
            self.ser.write(chr(col))
            self.ser.write(row.tostring())
            time.sleep(.01)

    def setPixelColor(self, row, col, color):
        self.buffer[row, col] = color
        
    def getPixelColor(self, i):
        return self.buffer[i]

    def update1(self, row, col, color):
        '''
        Update a single pixel
        '''
        self.buffer[row, col] = color

    def setAll(self, color):
        self.buffer[:,0] = color[0]
        self.buffer[:,1] = color[1]
        self.buffer[:,2] = color[2]
    def off(self):
        self.buffer *= 0
        self.show()
        
    def rotate(self, n):
        save = self.buffer[:n]
        self.buffer[:-n] = self.buffer[n:]
        self.buffer[-n:] = save
        self.show()
    
    def __enter__(self):
        pass
    def __exit__(self, *args):
        self.off()
def wheel(WheelPos, imax):
    ''' 
    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    '''
    if(WheelPos < 85):
        r = WheelPos * 3
        g = 255 - WheelPos * 3
        b = 0
    elif(WheelPos < 170):
        WheelPos -= 85
        r = 255 - WheelPos * 3
        g = 0
        b = WheelPos * 3
    else:
        WheelPos -= 170
        r = 0
        g = WheelPos * 3
        b = 255 - WheelPos * 3
    r = r * imax / 255
    g = g * imax / 255
    b = b * imax / 255
    return Color(r, g, b)

def test():
    N = 64
    buffer = numpy.zeros((N, 3), numpy.byte)
    strip = NeoPixel(N, '/dev/ttyUSB0', A5)
    with strip:
        RED = Color(25, 0, 0)
        GREEN = Color(0, 25, 0)
        BLUE = Color(0, 0, 25)
        WHITE = Color(255, 255, 255)
        colors = [RED, GREEN, BLUE, WHITE]
        
        if True: # wheel
            for i in range(N):
                strip.setAll(wheel(i * 255 / N, 255))
            strip.show()
        if True: # R, G, B
            for i in range(1):
                for color in colors:
                    strip.setAll(color)
                strip.show()
                time.sleep(1)

        if False: ## colors one pix at a time
            for color in colors:
                for row in range(8):
                    for col in range(N):
                        strip.update1(row, col, color)
        if True: ## bright rainbow
            for intensity in arange(10, 25, 5.):
                for row in range(8):
                    for col in range(N):    
                        strip.update1(row, col, wheel(i * 255 / N, intensity));
                strip.show()
        for i in range(0):
            strip.rotate(30)
        strip.off()
        around = 10
        while 1:
            for color in colors:
                strip.buffer[-2 * around::around] = color
                for i in range(25):
                    strip.rotate(around)

        raw_input('...')
        

if __name__ == '__main__':
    test()
