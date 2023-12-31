import os
import RPi.GPIO as GPIO
import time
from datetime import datetime

#Including code to send an email through gmail 
import smtplib
from email.mime.text import MIMEText

sender = "email@gmail.com"
recipients = ["email1@gmail.com", "email2@gmail.com"]
password = "" # generate an app password and save here
#End


from config import (NUMBER_OF_DOORS, SENSORS_PER_DOOR)

logfile = open("/home/mike/SiriGarage/static/log.txt","a")
logfile.write(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))
logfile.close()
print(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))

print(" Control + C to exit Program")
print(" Number of Doors: " + str(NUMBER_OF_DOORS))
print(" Number of Sensors Per Door: " + str(SENSORS_PER_DOOR))


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # Door 1 is Closed sensor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # Door 1 is Open sensor
GPIO.setup(29, GPIO.IN, GPIO.PUD_UP) # Door 2 is Closed sensor
GPIO.setup(31, GPIO.IN, GPIO.PUD_UP) # Door 2 is Open sensor
GPIO.setup(33, GPIO.IN, GPIO.PUD_UP) # Door 3 is Closed sensor
GPIO.setup(37, GPIO.IN, GPIO.PUD_UP) # Door 3 is Open sensor
time.sleep(1)

TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')  #Default Time
Door1_OpenTimer = 0  		#Default start status turns timer off
Door1_OpenTimerMessageSent = 1 	#Turn off messages until timer is started
Door1_CurrentState = 2          #It will reset to the correct value after the first run
Door2_OpenTimer = 0  		#Default start status turns timer off
Door2_OpenTimerMessageSent = 1  #Turn off messages until timer is started
Door3_OpenTimer = 0  		#Default start status turns timer off
Door3_OpenTimerMessageSent = 1  #Turn off messages until timer is started

TimeDoor1_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
TimeDoor2_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
TimeDoor3_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

try:
	while 1 >= 0:
		time.sleep(30) # change back to 30 after testing
		if Door1_OpenTimer != 0:  #Door Open Timer has Started
			currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
			if (currentTimeDate - TimeDoor1_Opened).seconds > 300 and Door1_OpenTimerMessageSent == 0:
				print("Your Garage Door 1 has been Open for " + str((currentTimeDate - TimeDoor1_Opened).seconds) + " seconds. TimeDoor1 Opened " + str(TimeDoor1_Opened))
				print(TimeDoor1_Opened)
				logfile = open("/home/mike/SiriGarage/static/log.txt","a")
				logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- 5  min warning Door 1 Open since " + str( TimeDoor1_Opened) + "\n") )
				logfile.close()

				subject = "URGENT Garage Door open since " + str( TimeDoor1_Opened) 
				body = "Close the door already!! It's been more than 5 minutes"

				def send_email(subject, body, sender, recipients, password):
					msg = MIMEText(body)
					msg['X-Priority'] = '1'
					msg['Subject'] = subject
					msg['From'] = sender
					msg['To'] = ', '.join(recipients)
					with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
						smtp_server.login(sender, password)
						smtp_server.sendmail(sender, recipients, msg.as_string())
					print("Message sent!")

				send_email(subject, body, sender, recipients, password)
				Door1_OpenTimerMessageSent = 0 #needs set back to 1 if you only want it to send an email once. only fires after timeopened  is greater than above.

		if Door2_OpenTimer != 0:  #Door Open Timer has Started
			currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
			if (currentTimeDate - TimeDoor2_Opened).seconds > 900 and Door2_OpenTimerMessageSent == 0:
				print("Your Garage Door #2 has been Open for 15 minutes")
				Door2_OpenTimerMessageSent = 1
		if Door3_OpenTimer != 0:  #Door Open Timer has Started
			currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
			if (currentTimeDate - TimeDoor3_Opened).seconds > 900 and Door3_OpenTimerMessageSent == 0:
				print("Your Garage Door #3 has been Open for 15 minutes")
				Door3_OpenTimerMessageSent = 1

#------------------------------- Door 1 Code -------------------------------

		if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:  #Door Status is Unknown (or Open if 1 Sensor Per Door)
			logfile = open("/home/mike/SiriGarage/static/log.txt","a")				#Start Door Open Timer
			if Door1_OpenTimer == 0:
				TimeDoor1_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
				Door1_OpenTimer = 1
				Door1_OpenTimerMessageSent = 0

			if SENSORS_PER_DOOR == 1:
				logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Open since " + str( TimeDoor1_Opened) + "\n") )
				print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Open since " + str( TimeDoor1_Opened) + "\n") )

			else:
				logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Opening/Closing \n"))
				print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Opening/Closing"))
			logfile.close()
		else:
			while GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
				time.sleep(.5)
			else:
				if GPIO.input(16) == GPIO.LOW:  #Door is Closed
					if Door1_CurrentState != 0: # Door was already closed, don't keep logging it.
						TimeDoor1_Closed = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
						logfile = open("/home/mike/SiriGarage/static/log.txt","a")
						logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Closed since " + str( TimeDoor1_Opened) + "\n") )
						logfile.close()
						print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Closed since " + str( TimeDoor1_Opened) + "\n") )
						Door1_OpenTimer = 0

				if GPIO.input(18) == GPIO.LOW:  #Door is Open
					logfile = open("/home/mike/SiriGarage/static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Open line 2 \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door 1 Open line 2"))
					#Start Door Open Timer
					TimeDoor1_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
					Door1_OpenTimer = 1
					Door1_OpenTimerMessageSent = 0
		Door1_CurrentState = Door1_OpenTimer

#------------------------------- Door 2 Code -------------------------------

		if NUMBER_OF_DOORS > 1:
			if GPIO.input(29) == GPIO.HIGH and GPIO.input(31) == GPIO.HIGH:  #Door Status is Unknown (or Open if 1 Sensor Per Door)
				if Door2_OpenTimer == 0:
					logfile = open("static/log.txt","a")
				if SENSORS_PER_DOOR == 1:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open"))
				else:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Opening/Closing \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Opening/Closing"))
				logfile.close()
				Door2_OpenTimer = 1
			else:
				while GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
					time.sleep(.5)
				else:
					if GPIO.input(29) == GPIO.LOW:  #Door is Closed
						logfile = open("static/log.txt","a")
						logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Closed \n"))
						logfile.close()
						print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Closed"))
						Door2_OpenTimer = 0

				if GPIO.input(31) == GPIO.LOW:  #Door is Open
					logfile = open("static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open"))
					#Start Door Open Timer
					TimeDoor2_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
					Door2_OpenTimer = 2
					Door2_OpenTimerMessageSent = 0

#------------------------------- Door 3 Code -------------------------------

		if NUMBER_OF_DOORS > 2:
			if GPIO.input(33) == GPIO.HIGH and GPIO.input(37) == GPIO.HIGH:  #Door Status is Unknown (or Open if 1 Sensor Per Door)
				if Door3_OpenTimer == 0:
					logfile = open("static/log.txt","a")
				if SENSORS_PER_DOOR == 1:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open"))
				else:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Opening/Closing \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Opening/Closing"))
				logfile.close()
				Door3_OpenTimer = 1
			else:
				while GPIO.input(33) == GPIO.HIGH and GPIO.input(37) == GPIO.HIGH:
					time.sleep(.5)
				else:
					if GPIO.input(33) == GPIO.LOW:  #Door is Closed
						logfile = open("static/log.txt","a")
						logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Closed \n"))
						logfile.close()
						print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Closed"))
						Door3_OpenTimer = 0

				if GPIO.input(37) == GPIO.LOW:  #Door is Open
					logfile = open("static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open"))
					#Start Door Open Timer
					TimeDoor2_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
					Door3_OpenTimer = 2
					Door3_OpenTimerMessageSent = 0



except KeyboardInterrupt:
	logfile = open("/home/mike/SiriGarage/static/log.txt","a")
	logfile.write(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
	logfile.close()
	print(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
	GPIO.cleanup()
