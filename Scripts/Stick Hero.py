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

    pixels = [list(i[:3]) for i in image[1400]]

    transitions = []
    ignore = True
    black = True

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        if ignore and (r + g + b) != 0:
            continue

        ignore = False

        if black and (r + g + b) != 0:
            black = not black
            print(i)
            transitions.append(i)
            continue

        if not black and (r + g + b) == 0:
            black = not black
            transitions.append(i)
            continue

    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 - target1
    distance = (gap + target) * 1.3

    print(f'transition points: {transitions}, distance: {distance}')

    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')

    time.sleep(2.5)

