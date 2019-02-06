#!/usr/bin/env python3

import requests
import json
import time
import datetime
from pygame import mixer
from os import walk
from os import listdir
from os.path import isfile, join
from random import randint


class ButtonQuery():
    website = 'http://bfitzy2142.appspot.com'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    rsvp_stat = {"Status": "init"}
    file_path = '/home/bfitzy/Music/'
    data_sent = {'playing': ''}

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
        while(True):

            webstat = self.api_handler('GET')
            svr_stat = webstat['Status']
            rsvp = self.rsvp_stat['Status']

            if (svr_stat == True and rsvp == 'init'):
                response = self.api_handler('POST')
                print(type(response))
                self.rsvp_stat = json.loads(response.text)
                print('Ping from website @' + str(datetime.datetime.now()))
                self.play_sound(self.current_sound)

            if (svr_stat == False and rsvp == 'Success'):
                self.rsvp_stat = {"Status": "init"}

            time.sleep(2)

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
        mixer.init()
        mixer.music.load(self.file_path + sound)
        mixer.music.play()
        while mixer.music.get_busy() == 1:
            continue


if (__name__ == "__main__"):
    notifier = ButtonQuery()
