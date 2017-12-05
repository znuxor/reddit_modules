#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Based on himawaripy by boramalper
# fetches a random wallpaper on reddit, applies it

import praw
import random
import requests
import subprocess
import os
import platform
import pickle

wallpaperLocation = os.path.join(os.path.expanduser('~'), 'Pictures', 'wallpaper')
subredditList = ['wallpapers', 'wallpaper']

random.shuffle(subredditList)
os.chdir(wallpaperLocation)
# os.environ['DBUS_SESSION_BUS_ADDRESS'] = "unix:path=/run/dbus/system_bus_socket"
os.environ["DISPLAY"] = ":0"
os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"
r  = praw.Reddit(user_agent='wallpaper getter by u/znuxor')
for theSubreddit in subredditList:
    submissions = list(r.get_subreddit(theSubreddit).get_hot(limit=25))
    random.shuffle(submissions)
    imageName = None
    for submission in submissions:
        if (('1920' in submission.title and '1080' in submission.title) or ('2560' in submission.title and '1440' in submission.title) or ('3840' in submission.title and '2160' in submission.title)) and submission.score > 0 and 'imgur' in submission.url and '/a/' not in submission.url:
            imageName = submission.url[::-1].split('/')[0][::-1]
            if '.jpg' not in submission.url and '.png' not in submission.url:
                subprocess.run(['wget', '-q', submission.url + '.png'], check=True)
            else:
                subprocess.run(['wget', '-q', submission.url], check=True)
            break
    if imageName is not None:
        break

if imageName is None:
    print('failed')
    quit()

filePath = os.path.join(wallpaperLocation, imageName)

''' Command per https://github.com/boramalper/himawaripy/issues/57
    Sets 'FillMode' to 1, which is "Scaled, Keep Proportions"
    Forces 'Color' to black, which sets the background colour.
'''
script = 'var a = desktops();' \
         'for (i = 0; i < a.length; i++) {{' \
         'd = a[i];d.wallpaperPlugin = "org.kde.image";' \
         'd.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");' \
         'd.writeConfig("Image", "file://{}");' \
         'd.writeConfig("FillMode", 1);' \
         'd.writeConfig("Color", "#000");' \
         '}}'
try:
    subprocess.check_output(["qdbus", "org.kde.plasmashell", "/PlasmaShell",
                             "org.kde.PlasmaShell.evaluateScript", script.format(filePath)])
except subprocess.CalledProcessError as e:
    if "Widgets are locked" in e.output.decode("utf-8"):
        print("!! Cannot change the wallpaper while widgets are locked.")
        print("!! Please unlock widgets to allow wallpaper changing.\n")
    else:
        print(e)
