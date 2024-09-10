I added a 10 minute delay on boot by adding this line to /boot/config.txt.  That way my network gear can boot up after a power loss.
boot_delay=600


YouTube Video Instructions found here: https://youtu.be/wfsYFM-9Dns

Setting up a Flask web server to control your garage door & display the door status & log usage. This Setup can control up to 3 garage doors and can also be controlled using Siri on you iPhone & Apple Watch

--------------------------------------------------------------------
Products I used in this video:
--------------------------------------------------------------------

Raspberry Pi Zero W with case on Amazon: https://amzn.to/34ujK5C

Raspberry Pi Zero W on Adafruit: https://www.adafruit.com/product/3400

4 Channel Relay (to Open Garage Door): https://amzn.to/3b4lHbD

Magnetic Reed Switch (You need at least 1 per door, 2 per door recommended): https://amzn.to/39YG7kU

Jumper/Breadboard wire 120ct: https://amzn.to/2V3fFlV

Hammer Header & Install Kit on Amazon: https://amzn.to/3b5RbxX

Hammer Headers on Adafruit: https://www.adafruit.com/product/3662

--------------------------------------------------------------------
Setup Instructions:
--------------------------------------------------------------------

1.  First setup your Raspberry Pi: https://www.youtube.com/watch?v=EeEU_8HG9l0 
2.  Lets upgrade the apt-get program:
    - sudo apt-get update

3.  To Allow us to use the GPIO pins on the Pi:
    - sudo apt-get install rpi.gpio

4.  Next install the Flask Web Server: 
    - sudo apt-get install python3-pip
    - sudo pip3 install flask

5.  Install the GIT application so you can download my Github code: 
    - sudo apt-get install git 

6.  Download my Github code: 
    - sudo git clone https://github.com/shrocky2/SiriGarage
 
7.  Test out setup and webpage (default port is 5001)
    - cd SiriGarage
    
    Test Relay connections
    - sudo python3 relaytest.py
    
    Test Magnetic Reed Switches
    - sudo python3 log.py
    
    Test out Webpage
    - sudo python3 siriweb.py
      - Open your web browser to: Rasp_Pi_IP_Address:5001

 8.  To Change Settings, including renaming doors, passwords, enabling Siri, & Setting Program to AutoStart on Boot:
     - Open your web browser to: Rasp_Pi_IP_Address:5001/Settings
     - Default Username:Password are admin:admin

9.  To Setup your iPhone & Apple Watch to control the garage door, follow the steps at:
    - Rasp_Pi_IP_Address:5001/page/sirisetup.html

10.  Setup the Pi to autostart when the Pi boots.
     - ran sudo crontab -e added these three lines:            
            # sleep is to give the network enough time to start.  Otherwise I was getting 127.0.0.1
            @reboot sleep 60 && sudo python3 /home/mike/SiriGarage/siriweb.py &
            @reboot sleep 60 && sudo python3 /home/mike/SiriGarage/log.py &

     - sudo nano /etc/rc.local
     - Enter the 2 lines of code found on Rasp_Pi_IP_Address:5001/Settings before the last line that says "Exit 0"
     - Control + X (to exit and save)

11.  Reboot system and let program autostart
     - sudo reboot

12.  ***Not Recommended*** Setup a VPN connection to your router instead.Set up Port Forwarding on your Router to allow access when away from home. (please note that this program is not a secure website (https), so it's best not to connect to this program on a public network like a coffee shop or hotel.)
     - You'll need to setup PORT FORWARDING on your home router to pass traffic from the internet to the Raspberry Pi.
     - Check out this video for help with port forwarding: https://youtu.be/VhVV25zCFrQ
     - To find out your External IP Address, Check this link: https://checkip.amazonaws.com
     - Setup Siri using your External IP Address and the Port Number you setup in Port Forwarding.
     - Once setup, turn off WiFi on your phone and test. You'll need to know the EXTERNALL address of your home router.

13. I modified the original to include an email option and made some changes so I could open it slightly differently.

--------------------------------------------------------------------
Wiring Diagram:
--------------------------------------------------------------------

<img src="https://github.com/shrocky2/SiriGarage/blob/main/static/images/Multi_Door_Wiring_Diagram.jpg">

--------------------------------------------------------------------
Additional Videos:
--------------------------------------------------------------------
My Original Raspberry Pi Controlled Garage Door Video: https://youtu.be/Fcx6wANw9KM

Sonoff Garage Door Opener: https://youtu.be/f1JeKHraDf8

How to set up your Raspberry Pi: https://youtu.be/EeEU_8HG9l0

How to set up Port Forwarding on your Router: https://youtu.be/VhVV25zCFrQ
