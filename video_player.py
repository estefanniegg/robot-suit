#This script has three threads, one for the Instagram function, one for the video player and one for the button. 
#When the Instagram button is pressed, a blank video is played until the number of likes on the latest post increases.  When an increase is detected, a video of a electrocardiogram heartbeat plays.
#When the video button is pressed, the script plays a video.  Each press cycles through a predefined set of videos.

import requests
import json
import re
import time
import threading 
import os
import sys
import subprocess
import RPi.GPIO as GPIO
from subprocess import Popen

users = ['estefanniegg']

buttonPin = 7
buttonPin2 = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(buttonPin2, GPIO.IN)

birthdayRobot = ("/home/pi/birthdayRobotMinute.mp4")
heartVideo= ("/home/pi/BeatMinute.mp4")
partyRobotVideo= ("/home/pi/partyRobotMinute.mp4")
chillingVideo = ("/home/pi/chillingRobot.mp4")
sadVideo = ("/home/pi/sadRobot.mp4")

condition = threading.Condition()
videoToPlay = 0

mode = 0
liveVideo = ("/home/pi/beat.mp4")
deadVideo = ("/home/pi/black.mp4")
previous_like_count = 0
current_like_count = 0

def buttonThread():
    global mode
    while True:
        condition.acquire()
        buttonState = GPIO.input(buttonPin)
        buttonState2 = GPIO.input(buttonPin2)

        global videoToPlay
        if buttonState != 0:
            mode = 0
            if videoToPlay < 4:
                videoToPlay = videoToPlay + 1
            else:
                videoToPlay = 0
            condition.notifyAll()
            condition.release()
	    
            time.sleep(0.3)
        elif buttonState2 != 0:
            mode = 1
            condition.notifyAll()
            condition.release()
            time.sleep(0.3)
        else:
            condition.release()
            
def instagramThread():
    global mode
    global liveVideo
    global deadVideo
    global previous_like_count
    global current_like_count

    while True:
        if mode == 1:
            condition.acquire()
            for user in users:
                page = requests.get('https://www.instagram.com/' + user + '/')        
                # finding first post
                text = page.text
        
                 # find where the posts start
                finder_text_start = ('<script type="text/javascript">'
                                     'window._sharedData = ')
                finder_text_start_len = len(finder_text_start) - 1
                finder_text_end = ';</script>'
        
                all_data_start = text.find(finder_text_start)
                all_data_end = text.find(finder_text_end, all_data_start + 1)
                json_str = text[(all_data_start + finder_text_start_len + 1) \
                                : all_data_end]
                all_data = json.loads(json_str)
        
                # this puts posts into a list
                media_by_tag = list(all_data['entry_data']['ProfilePage'][0] \
                                            ['user']['media']['nodes'])
        
                # first post
                print ('https://www.instagram.com/p/' + media_by_tag[0]['code'] + '/')
                postpage = requests.get('https://www.instagram.com/p/' + media_by_tag[0]['code'] + '/')
                postcontent = postpage.content
                filtered = re.search(r"\"edge_media_preview_like\": {\"count\": \d+", postcontent)
                likecount = re.search('(?<=t\": )\d+', filtered.group(0))
                intlikecount = int(likecount.group(0))

                current_like_count = intlikecount

                os.system('killall omxplayer.bin')

                if current_like_count > previous_like_count:
                    omxc = Popen(['omxplayer', '-b', liveVideo])
                    #time.sleep(4)
                    condition.wait(4)
                else:
                    omxc = Popen(['omxplayer', '-b', deadVideo])
                    #time.sleep(1)
                    condition.wait(1)

                print current_like_count
                previous_like_count = current_like_count
            condition.release()


def videoThread():
    global videoToPlay
    global mode
    while True:
        condition.acquire()
        if mode == 0:
            os.system('killall omxplayer.bin')
            if videoToPlay == 0:
                omxc = Popen(['omxplayer', '-b', birthdayRobot])
            elif videoToPlay == 1:
                omxc = Popen(['omxplayer', '-b', heartVideo])
            elif videoToPlay == 2:
                omxc = Popen(['omxplayer', '-b', partyRobotVideo])
            elif videoToPlay == 3:
                omxc = Popen(['omxplayer', '-b', chillingVideo])
            elif videoToPlay == 4:
                omxc = Popen(['omxplayer', '-b', sadVideo])
        
            condition.wait(60)
        condition.release()
 
bt = threading.Thread(target=buttonThread)
vt = threading.Thread(target=videoThread)
igt = threading.Thread(target=instagramThread)
vt.start()
bt.start()
igt.start()
