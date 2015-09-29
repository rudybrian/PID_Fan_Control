# PID_Fan_Control
Automatic temperature control for fans attached to a Raspberry Pi

This code is only a proof of concept and would need to be modified to some degree to be adequately usable.

## Notes
* The Wikipedia article on PID controllers: https://en.wikipedia.org/wiki/PID_controller
* Requires WiringPi2-Python (https://github.com/Gadgetoid/WiringPi2-Python) 
* The user executing this script must be added to the video and spi groups to have sufficient privileges to run
* The temperature is actually coming from the GPU, but the GPU and CPU temps should be roughly the same
* The PiFace ULN2803A is only capable of driving 500mA max on each output, so if you need to drive a high power fan, appropriate drive circuitry must be added to the output 
* If driving a two or three wire 12V fan directly from a PiFace output, you will need to remove jumper 4 (disables built-in snubber diodes connected to +5V) or you risk damaging your PiFace. You will also need to use a snubber diode across the fan motor's windings to prevent inductive kickback from causing problems. If driving a four wire (PWM) fan, the current source only needs to supply 5mA, can use 5V, does not require a snubber diode or the removal of jumper 4.

## Configuration
The three adjustable parameters are:
* PIN_TO_PWM: This parameter is the GPIO pin to use for PWM. Default is 202 (PiFace output #3)
* TEMP_SET_POINT: This is the target temperature in Celsius. Default is 45.0
* INVERT_DUTY_CYCLE: This parameter is used to invert the duty cycle which is needed if using open collector outputs (like the PiFace) to drive a four wire (PWM) fan. Default is False.
* MIN_FAN_SPEED: This parameter is used to set the minimum duty cycle. Some fans do not spin with the duty cycle below certain values, and this allows setting a minimum value to avoid this. Default is 0.
* MIN_FAN_TURN_OFF: This parameter works in conjunction with MIN_FAN_SPEED to turn off the fan when the target duty cycle reaches 0. Default is False.
