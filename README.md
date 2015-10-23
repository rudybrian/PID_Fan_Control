# PID_Fan_Control
Automatic temperature control for fans attached to a Raspberry Pi

## Notes
* The Wikipedia article on PID controllers: https://en.wikipedia.org/wiki/PID_controller
* Requires WiringPi2-Python (https://github.com/Gadgetoid/WiringPi2-Python) 
* The user executing this script must be added to the video and spi groups to have sufficient privileges to run
* The temperature is actually coming from the GPU, but the GPU and CPU temps should be roughly the same
* The PiFace ULN2803A is only capable of driving 500mA max on each output, so if you need to drive a high power fan, appropriate drive circuitry must be added to the output 
* If driving a two or three wire 12V fan directly from a PiFace output, you will need to remove jumper 4 (disables built-in snubber diodes connected to +5V) or you risk damaging your PiFace. You will also need to use a snubber diode across the fan motor's windings to prevent inductive kickback from causing problems. If driving a four wire (PWM) fan, the current source only needs to supply 5mA, can use 5V and does not require a snubber diode or the removal of jumper 4.

## Configuration
The adjustable parameters are:
* -l LOG, --log LOG
	The file to write the logs to. Default is /home/fpp/media/logs/pid_fan_control.log. 
* -p PWM_PIN, --pwm_pin PWM_PIN
	This parameter sets the GPIO output to use for PWM. Default is 202 (PiFace output #3)
* -t TEMP, --temp TEMP
	This is the target temperature in Celsius. Default is 45.0
* -i, --invert
	This parameter is used to invert the duty cycle which is needed if using open collector outputs (like the PiFace) to drive a four wire (PWM) fan. Default is False.
* -m MIN_SPEED, --min_speed MIN_SPEED 
	This parameter is used to set the minimum duty cycle. Some fans do not spin with the duty cycle below certain values, and this allows setting a minimum value to avoid this. Default is 0.
* -o, --min_turn_off
	This parameter works in conjunction with MIN_FAN_SPEED to turn off the fan when the target duty cycle reaches 0. Default is False.
* -v, --verbose
	Verbose logging. When enabled, this parameter instructs the program to log additional details during run time which can be helpful when setting up new fans, or tuning parameters. Default is False.
* -T VERBOSE_TEMP_THRESHOLD, --verbose_temp_threshold VERBOSE_TEMP_THRESHOLD
	When using verbose logging, the amount the temperature must change (+-) to write to the logfile if the duty cycle has not changed. This can be helpful if using the logs to monitor the fan/temperature performance. Default is 1.0

## Installation
FPP users: to make the script run as a daemon, follow the instructions below.
  1. Upload the two python (.py) files to your FPP scripts directory (/home/fpp/media/scripts)
  2. Upload the init script (.sh) to your uploads directory.
  3. SSH in to your FPP.
    1. Manually run the PID_fan_control.py script to ensure it works properly, and add/adjust any configurable parameters via command line options. It may be helpful to enable verbose logging (--verbose) to see more details while running. You can view the logs in the FPP log directory under the name PID_fan_control.log.
    2. Only once you are satisfied with the settings, continue to the next step.
    3. Copy the init script to your init.d directory with `sudo cp /home/fpp/media/uploads/PID_fan_control.sh /etc/init.d`.
    4. Make the init script executable with 'sudo chmod 755 /etc/init.d/PID_fan_control.sh'
    5. Edit the init script and add any desired command line arguments to DAEMON_OPTS. e.g. `DAEMON_OPTS="--min_speed 85 --min_turn off"`
    6. Verify that the script is working by running the following `sudo /etc/init.d/PID_fan_control.sh start`, then `sudo /etc/init.d/PID_fan_control.sh status` this should show that the program is running. Also, confirm it is using the desired settings by looking at the most recent log entry in PID_fan_control.log in your FPP Logs.
    7. Once you are happy with how things are working, run `sudo update-rc.d PID_fan_control.sh defaults` This will add the symbolic links to your rc directories and make the program automatically start/stop at the appropriate times.
    8. Reboot FPP and ensure the daemon is running by checking the latest log entry, and confirming the `python /home/fpp/media/scripts/PID_fan_control.py` process is running from the FPP Troubleshooting Commands in the Processes section.

## References
* This application was initially based on pidfanpi: https://github.com/SimplyAutomationized/raspberrypi/tree/master/pidfanpi
* Extensive re-use of example code from http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

