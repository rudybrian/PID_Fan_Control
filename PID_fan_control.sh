#!/bin/sh

### BEGIN INIT INFO
# Provides:          PID_fan_control
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple PID loop to control fan speed based on temperature
# Description:       Simple PID loop to control fan speed based on temperature
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
DIR=/home/fpp/media/scripts
DAEMON=$DIR/PID_fan_control.py
DAEMON_NAME=PID_fan_control

# Add any command line options for your daemon here
#DAEMON_OPTS="--min_turn_off --min_speed 85"
#DAEMON_OPTS="--min_turn_off --min_speed 85 --verbose --verbose_temp_threshold 0.1"
DAEMON_OPTS="--min_turn_off --min_speed 0 --on_off --verbose --verbose_temp_threshold 0.1"

# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=fpp

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
