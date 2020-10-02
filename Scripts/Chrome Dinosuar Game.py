from ppadb.client import Client
from PIL import Image
import numpy
import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

while True:
    image = device.screencap()

    with open('screenshots/screen.png', 'wb') as f:
        f.write(image)

    image = Image.open('screenshots/screen.png')
    image = numpy.array(image, dtype=numpy.uint8)

    pixels = [list(i[:3]) for i in image[470]]

    print(pixels)

    pl = False
    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        if r == 83 and i >= 336:
            print(r)
            print(g)
            print(b)
            print(i)
            device.shell(f'input touchscreen swipe 300 460 300 460 10')
            break



