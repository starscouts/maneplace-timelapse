import json
import time
import shutil
import os
import datetime
from PIL import Image

divider = 60
dates = {}

try:
    shutil.rmtree("./frames")
except FileNotFoundError:
    pass

os.mkdir("./frames")

data = json.load(open('data.json'))
image = Image.open('initial.png')
initial = Image.open('initial.png')
image.save('frames/0000000000000000.png')

total = len(data)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


colors = [
    "#6D001A",
    "#BE0039",
    "#FF4500",
    "#FFA800",
    "#FFD635",
    "#FFF8B8",
    "#00A368",
    "#00CC78",
    "#7EED56",
    "#00756F",
    "#009EAA",
    "#00CCC0",
    "#2450A4",
    "#3690EA",
    "#51E9F4",
    "#493AC1",
    "#6A5CFF",
    "#94B3FF",
    "#811E9F",
    "#B44AC0",
    "#E4ABFF",
    "#DE107F",
    "#FF3881",
    "#FF99AA",
    "#6D482F",
    "#9C6926",
    "#FFB470",
    "#000000",
    "#515252",
    "#898D90",
    "#D4D7D9",
    "#FFFFFF",
    "#ffff5c",
    "#d9d94a",
    "#ff7313",
    "#fce07c",
    "#bdbd3e",
    "#c0aa19",
    "#8f8fe0",
    "#6b6bd1",
    "#9efe90",
    "#360082",
    "#00ccff",
    "#44b1ce",
    "#4a2157",
    "#d676e3",
    "#abfbff",
    "#a11461",
    "#592d1b",
    "#914724",
    "#cc6d42",
    "#ff8559",
    "#ffd5ad",
    "#d39748",
    "#fa74a4",
    "#ffd1dc",
    "#679112",
    "#d39648",
    "#9fc455",
    "#d5ebad",
    "#adafb0",
    "#793ccf",
    "#a771f7",
    "#d3bff5",
]

frame = 1
frameFile = 1
times = []

for event in data:
    percentage = "%.2f" % ((frame / total) * 100)
    remaining = total - frame

    if len(times) > 0:
        avg = sum(times) / len(times)
    else:
        avg = 0

    eta = None

    if frame > 1000:
        eta = avg * remaining

    if eta is not None:
        eta_seconds = round(eta / 1000000000)
        eta_string = str(eta_seconds) + " seconds remaining"
        done_by = datetime.datetime.fromtimestamp(round(time.time() + eta_seconds)).isoformat().split("T")[1]

        if eta_seconds > 60:
            if eta_seconds > 3600:
                if round(eta_seconds / 3600) > 1:
                    eta_string = str(round(eta_seconds / 3600)) + " hours remaining"
                else:
                    eta_string = str(round(eta_seconds / 3600)) + " hour remaining"
            else:
                if round(eta_seconds / 60) > 1:
                    eta_string = str(round(eta_seconds / 60)) + " minutes remaining"
                else:
                    eta_string = str(round(eta_seconds / 60)) + " minute remaining"

        print(f"\r{frame}/{total} ({percentage}% complete, {eta_string}, done at {done_by})", end="", flush=True)
    else:
        print(f"\r{frame}/{total} ({percentage}% complete, calculating...)", end="", flush=True)

    start = time.time_ns()
    if 'x' in event and 'y' in event:
        # Normal pixel placement
        if colors[event['color']] is not None and event['userId'] != "591555636505083905":
            image.putpixel((event['x'], event['y']), hex_to_rgb(colors[event['color']]))
    else:
        # Mod tool
        if 0 <= event['x1'] <= 1000 and 0 <= event['x2'] <= 1000 \
                and 0 <= event['y1'] <= 1000 and 0 <= event['y2'] <= 1000:
            for x in range(event['x1'], event['x2']):
                for y in range(event['y1'], event['y2']):
                    if colors[event['color']] is not None:
                        image.putpixel((x, y), hex_to_rgb(colors[event['color']]))
        else:
            print(event)

    if frame % divider == 0:
        image.save(f'frames/{str(frameFile).rjust(16, "0")}.png')
        dates[str(frameFile / 60)] = event['timestamp']
        frameFile += 1

    frame += 1

    end = time.time_ns()
    duration = end - start
    times.append(duration)

print("\r\nSaving video...")
os.system("ffmpeg -y -framerate 60 -pattern_type glob -i 'frames/*.png' -c:v libx264 out.pre.mp4")
os.system("ffmpeg -y -i out.pre.mp4 out.pre.webm")

print("\r\nSaving metadata...")
with open('metadata.json', 'w') as f:
    json.dump(dates, f)

print("\r\nSwitching slots...")
try:
    os.remove("out.old.mp4")
except FileNotFoundError:
    pass
os.rename("out.mp4", "out.old.mp4")
os.rename("out.pre.mp4", "out.mp4")

try:
    os.remove("out.old.webm")
except FileNotFoundError:
    pass
os.rename("out.webm", "out.old.webm")
os.rename("out.pre.webm", "out.webm")
