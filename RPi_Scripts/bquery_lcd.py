#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime
from pygame import mixer
from os import walk, listdir
from os.path import isfile, join
from random import randint
import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD


class ButtonQuery():
    website = 'http://bfitzy2142.appspot.com'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    rsvp_stat = {"Status": "init"}
    # change filepath to a folder containing mp3 files
    file_path = '/home/pi/Music/temp/'
    data_sent = {'playing': ''}
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    #  Initialize LCD (must specify pinout and dimensions)
    lcd = Adafruit_CharLCD(rs=26, en=19,
                           d4=13, d5=6, d6=5, d7=11,
                           cols=16, lines=2)
    requests = 0
    getRequests = 0

    def __init__(self):
        self.sounds = self.get_sounds()
        self.run()

    def run(self):
        """
        This is the main body of the program. Run calls the webserver
        after waiting two seconds to determine if the ping status is true;
        the status of the server is stored in svr_stat. If it is found to
        be true, and another request has not already been sent, the script
        will send the song to be played via a post api request to the webserver
        and start playing that audio for me to hear.

        Parameters:
        svr_stat (Server Status): Will be used to store the value of
        webstat['Status'] which contains a boolean indicating if the
        webserver button has been pressed or not.

        rsvp_stat (Reply Status): Used to store the value of the reply
        from the webserver's data api serving the post with the song to
        be played by the Raspberry Pi.
        """
        try:
            while(True):
                self.lcd.clear()
                webstat = self.api_handler('GET')
                self.getRequests += 1
                svr_stat = webstat['Status']
                self.lcd.message('GET:' + str(self.getRequests) + 
                              'RQ:' + str(self.requests) + '\n')
                self.lcd.message(datetime.now().strftime('%b %d %H:%M:%S'))
                svr_stat = webstat['Status']
                rsvp = self.rsvp_stat['Status']

                if (svr_stat == True and rsvp == 'init'):
                    self.requests += 1
                    response = self.api_handler('POST')
                    self.rsvp_stat = json.loads(response.text)
                    print('Ping from website @' + str(datetime.now()))
                    self.lcd.clear()
                    self.lcd.message('About to play:\n')
                    self.lcd.message(self.current_sound)
                    time.sleep(2)
                    for x in range(0, 16):
                        self.lcd.move_left()
                        time.sleep(.4)
                    self.play_sound(self.current_sound)
                    self.lcd.clear()

                if (svr_stat == False and rsvp == 'Success'):
                    self.rsvp_stat = {"Status": "init"}

                time.sleep(2)

        except KeyboardInterrupt:
            print('\nCTRL-C pressed.  Program exiting...')
            self.lcd.clear()

        finally:
            self.lcd.clear()
            GPIO.cleanup()

    def get_sounds(self):
        """
        Gets available sound tracks to be played

        Returns:
        List of files in file_path directory
        """
        track_list = []
        for files in walk(self.file_path):
            for filename in files:
                track_list.append(filename)
        # Index 2 contains items in parent directory
        return track_list[2]

    def api_handler(self, request_type):
        """
        Method to send and retrieve data from webapp api.

        Parameters:
        request_type: 
        'GET': to retrieve status from webapp.
        'POST': Send next song to play.

        Returns:
        /get-status: {"Status": 'True/False'}
        /data: Status code of post <Success> if okay. 
        """
        if (request_type is 'GET'):
            raw_request = requests.get(self.website + '/get-status')
            return raw_request.json()
        elif (request_type is 'POST'):
            self.current_sound = self.sounds[randint(0, len(self.sounds)-1)]
            data_sent = {'playing': self.current_sound}
            return requests.post(
                self.website + '/data',
                allow_redirects=False,
                data=json.dumps(data_sent),
                headers=self.headers)

    def play_sound(self, sound):
        """
        Play_sound is called to play an audio track passed in via
        the sound parameter.
        """
        GPIO.output(4, True)
        mixer.init()
        mixer.music.load(self.file_path + sound)
        mixer.music.play()
        while mixer.music.get_busy() == 1:
            continue
        GPIO.output(4, False)


if (__name__ == "__main__"):
    notifier = ButtonQuery()
