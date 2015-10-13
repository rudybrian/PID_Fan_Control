#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# PID_fan_control.py
# 
# Simple PID loop to control fan speed. 
#
#
# Copyright (C) 2015 Brian Rudy (Setarcos)
#
# PID_fan_control is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#

import subprocess
import logging
import logging.handlers
import argparse
import sys
import wiringpi2
import pid as pid
from time import sleep

# Defaults
PIN_TO_PWM = 202       		# PiFace output 3
TEMP_SET_POINT = 45.0  		# Temperature setpoint in Celsius
INVERT_DUTY_CYCLE = False	# Set to "True" if using a four wire (PWM) fan with open collector outputs (i.e. PiFace)
MIN_FAN_SPEED = 0		# Some fans don't work properly if you decrease the duty cycle below a certain value. 
MIN_FAN_TURN_OFF = False	# When using MIN_FAN_SPEED, allow the fan to turn off when duty cycle is 0.
LOG_FILENAME = "/home/fpp/media/logs/pid_fan_control.log"	# Default log file location
LOG_LEVEL = logging.INFO	# Default INFO level logging (could also be DEBUG or WARNING)
VERBOSE_LOGGING = False		# Log additional details to aid in initial setup/debugging

# Define the command line arguments
parser = argparse.ArgumentParser(description="Simple PID loop to control fan speed")
parser.add_argument("-l", "--log", help="File to write log to (default '" + LOG_FILENAME + "')")
parser.add_argument("-p", "--pwm_pin", help="Pin to use for PWM control (default '" + str(PIN_TO_PWM) + "')")
parser.add_argument("-t", "--temp", help="Temperature setpoint (default '" + str(TEMP_SET_POINT) + "')")
parser.add_argument("-i", "--invert", help="Invert duty cycle (default '" + str(INVERT_DUTY_CYCLE) + "')", action="store_true")
parser.add_argument("-m", "--min_speed", help="Minimum fan duty cycle (default '" + str(MIN_FAN_SPEED) + "')")
parser.add_argument("-o", "--min_turn_off", help="When using --min_speed with a value >0, set to True to turn off the fan when the target speed is 0 --min_speed (default '" + str(MIN_FAN_TURN_OFF) + "')", action="store_true")
parser.add_argument("-v", "--verbose", help="Verbose logging (default '" + str(VERBOSE_LOGGING) + "')", action="store_true")

# parse the command line arguments
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log
if args.pwm_pin:
	PIN_TO_PWM = int(args.pwm_pin)
if args.temp:
	TEMP_SET_POINT = float(args.temp)
if args.min_speed:
	MIN_FAN_SPEED = int(args.min_speed)

INVERT_DUTY_CYCLE = args.invert
MIN_FAN_TURN_OFF = args.min_turn_off
VERBOSE_LOGGING = args.verbose

# Set a unique name
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
	def __init__(self, logger, level):
		"""Needs a logger and a logger level."""
		self.logger = logger
		self.level = level

	def write(self, message):
		# only log if there is actually a message and not just a newline
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)


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
if VERBOSE_LOGGING:
	print "Result from piFaceSetup(200): {}".format(str(result))

pwm = wiringpi2.softPwmCreate(PIN_TO_PWM,cycle,100) # Setup PWM using Pin, Initial Value and Range parameters
if VERBOSE_LOGGING:
	print "Result from softPwmCreate(PIN_TO_PWM, cycle, 100): {}".format(str(pwm))

last_duty_cycle = 0

print 'Starting main loop with the following settings:'

# Defaults
print '->PIN_TO_PWM=' + str(PIN_TO_PWM)
print '->TEMP_SET_POINT=' + str(TEMP_SET_POINT)
print '->INVERT_DUTY_CYCLE=' +str(INVERT_DUTY_CYCLE)
print '->MIN_FAN_SPEED=' +str(MIN_FAN_SPEED)
print '->MIN_FAN_TURN_OFF=' +str(MIN_FAN_TURN_OFF)
print '->LOG_FILENAME=' + LOG_FILENAME 
print '->LOG_LEVEL=' +str(LOG_LEVEL)

while True:
	sleep(1)
	x = (p.update(get_temperature()))*-1
	#print x
	cycle = 100 + int(x)
	if (cycle < 0):
		cycle = 0
	elif (cycle > 100):
		cycle = 100

	if (MIN_FAN_TURN_OFF and cycle == 0):
		cycle = 0
	elif (cycle < MIN_FAN_SPEED):
		cycle = MIN_FAN_SPEED

	# Only print something when the duty cycle changes
	if (last_duty_cycle != cycle and VERBOSE_LOGGING):
		print 'Setpoint: ' +str(TEMP_SET_POINT)+ ', Temp: ' +str(get_temperature())+ ', Fan Speed: ',str(cycle)+'%'
		last_duty_cycle = cycle
	if INVERT_DUTY_CYCLE:
		wiringpi2.softPwmWrite(PIN_TO_PWM,100 - cycle) # Change PWM duty cycle
	else:
		wiringpi2.softPwmWrite(PIN_TO_PWM,cycle) # Change PWM duty cycle

