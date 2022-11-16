#! /bin/sh

### BEGIN INIT INFO
# Provides:          main.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Special sudo with access to original PATH
alias mysudo='sudo -E env "PATH=$PATH"'

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting matrix controller"
    mysudo python /usr/local/bin/pi-wall-art/src/main.py &
    ;;
  stop)
    echo "Stopping matrix controller"
    pkill -f /usr/local/bin/pi-wall-art/src/main.py
    ;;
  *)
    echo "Usage: /etc/init.d/rgbmatrix.sh {start|stop}"
    exit 1
    ;;
esac

exit 0

# Copy into /etc/init.d
# sudo cp rgbmatrix.sh /etc/init.d
# sudo update-rc.d rgbmatrix.sh defaults

# Manual start: sudo /etc/init.d/rgbmatrix.sh start

# Based on: https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi