# PID_Fan_Control
Automatic temperature control for fans attached to a Raspberry Pi

This code is only a proof of concept and would need to be modified to some degree to be adequately usable.

## Notes
* The Wikipedia article on PID controllers: https://en.wikipedia.org/wiki/PID_controller
* Requires WiringPi2-Python (https://github.com/Gadgetoid/WiringPi2-Python) 
* The fpp user must be added to group video and group spi to have sufficient privileges to run
* The temperature is actually coming from the GPU, but the GPI and CPU temps should be roughly the same
* The PiFace ULN2803A is only capable of driving 500mA max across all outputs, so if you need to drive a high power fan, appropriate drive circuitry must be added to the output 
* If driving a two or three wire 12V fan directly from a PiFace output, you will need to remove jumpers 4,5,6 and 7 or you risk damaging your PiFace. You will also need to use a snubber diode across the fan motor's windings to prevent inductive kickback from causing problems. If driving a four wire (PWM) fan, the current source only needs to supply 5mA, can use 5V, does not require a snubber diode or the removal of jumpers 4-7.
