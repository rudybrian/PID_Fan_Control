# -*- coding: utf-8 -*-
#
# PID_fan_control.py
# 
# Simple PID loop to control fan speed. 
#
# Originally based on pidfanpi: https://github.com/SimplyAutomationized/raspberrypi/tree/master/pidfanpi
#
## Release History
# v0.01 09/14/2015 Brian Rudy (brudyNO@SPAMpraecogito.com)
#	First working version. Only supports the Raspberry Pi and PiFace board. Uses the GPU temperature for reference.
#

import subprocess
import os
import wiringpi2
import pid as pid
from time import sleep

PIN_TO_PWM = 202       		# PiFace output 3
TEMP_SET_POINT = 45.0  		# Temperature setpoint in Celsius
INVERT_DUTY_CYCLE = False	# Set to "True" if using a four wire (PWM) fan with open collector outputs (i.e. PiFace)
MIN_FAN_SPEED = 0		# Some fans don't work properly if you decrease the duty cycle below a certain value. 
MIN_FAN_TURN_OFF = False	# When using MIN_FAN_SPEED, allow the fan to turn off when duty cycle is 0.

def get_temperature():
	# Returns the temperature in degrees Celsius
	try:
		s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
		return float(s.split('=')[1][:-3])
	except:
		print 'Unable to run vcgencmd!'
		return 0


# Main routine starts here
p = pid.PID(1,1,0.02, Integrator_max=100, Integrator_min=0)
p.setPoint(TEMP_SET_POINT)
cycle = 100 # Set the initial fan duty cycle to 100%

# Setup the PiFace PWM
wiringpi2.wiringPiSetupSys()
result = wiringpi2.piFaceSetup(200) # Must use the base address of the PiFace
print "Result from piFaceSetup(200): {}".format(str(result))

pwm = wiringpi2.softPwmCreate(PIN_TO_PWM,cycle,100) # Setup PWM using Pin, Initial Value and Range parameters
print "Result from softPwmCreate(PIN_TO_PWM, cycle, 100): {}".format(str(pwm))

print 'Starting main loop'
try:
	while True:
		sleep(1)
		#os.system('clear')
		x = (p.update(get_temperature()))*-1
		print x
		cycle = 100 + int(x)
		if (cycle < 0):
			cycle = 0
		elif (cycle > 100):
			cycle = 100

		if (MIN_FAN_TURN_OFF and cycle == 0):
			cycle = 0
		elif (cycle < MIN_FAN_SPEED):
			cycle = MIN_FAN_SPEED

		print 'Setpoint: ' +str(TEMP_SET_POINT)+ '\nTemp: ' +str(get_temperature())+ '\nFan Speed: ',str(cycle)+'%'
		if INVERT_DUTY_CYCLE:
			wiringpi2.softPwmWrite(PIN_TO_PWM,100 - cycle) # Change PWM duty cycle
		else:
			wiringpi2.softPwmWrite(PIN_TO_PWM,cycle) # Change PWM duty cycle
except KeyboardInterrupt:
	wiringpi2.softPwmWrite(PIN_TO_PWM,0) # Change PWM duty cycle to 0 (off)
	pass


