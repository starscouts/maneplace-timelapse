import sys

import json
import time
import os
from PIL import Image

try:
    os.mkdir("./users")
except FileExistsError:
    pass

data = json.load(open('data.json'))
users = []

for item in data:
    if item['userId'] not in users:
        users.append(item['userId'])


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


length = len(users)
index = 1

for user in users:
    image = Image.new(mode="RGB", size=(1000, 1000))

    frame = 1
    times = []

    for event in data:
        start = time.time_ns()
        if 'x' in event and 'y' in event and event['userId'] == user:
            image.putpixel((event['x'], event['y']), (255, 255, 255))

    print(f"Saving frame for {user} [{index}/{length}, {round((index / length) * 100, 2)}%]...")
    image.save(f'users/{user}.png')
    index += 1
