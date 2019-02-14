# bnotified

A simple flask webapp that's purpose is to notify me via random sound samples (Many of which were inspired by the 1999 American comedy film and cult classic Office Space). 

** How does my webapp work?
The bnotified project uses a client server model. The webapp component is the server providing the /data and /get-status API handlers. The Raspberry Pi acts as the client and runs the bquery python module. The bquery module continues indefinitely detecting the status reported through the /get-status handle. The webapp triggers a notification through a button press, changing the status to true. When /get-status returns true, the bquery module on the RPi sends a post request to the /data handle containing the string value that is the name of the soundtrack to be played, and then proceeds with playing that audio. When this string value is received via the post to /data, it is displayed on screen of the notifying user for twenty seconds. After this point, status is brought back to false allowing that user to renotify.

** What I learned?
Through this project I was able to gain exposure of full stack development with Flask, Python3, and JavaScript. The best takeaway was creating APIs and the RESTful protocol to communicate between components. However, it was also useful learning how to use AJAX and jQuery to display dynamic text/images without reloading the webpage. 

Additionally, I created a new bquery script (bquery_lcd.py) which displays statistics on a 16x02 display I have connected to the GPIO of my RPi. Somescreenshots are attached:

## Raspberry Pi Waiting for Website Request
![rpi_waiting](static/waiting.JPG?raw=true "Raspberry Pi Waiting for Website Request")

## Raspberry Pi Notified from Website
![rpi_notified](static/request_in.JPG?raw=true "Raspberry Pi Notified")

## Website View
![website](static/Website_view.PNG?raw=true "Website View")

## Website Notifying
![website-notifying](static/Website_notifying.PNG?raw=true "Website Notifying")
