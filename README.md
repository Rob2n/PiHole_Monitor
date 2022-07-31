# PiHole_Monitor
Display PiHole statistics on ssd1306 128x64 I²C LCD
> Inspired by [this tutorial](https://www.raspberrypi-spy.co.uk/2019/10/pi-hole-oled-status-screen/) but tweaked, updated for 2022 libraries and without LED

## Circuit Diagram
![Circuit Diagram](https://github.com/Rob2n/PiHole_Monitor/blob/main/PiHole_Monitor_sketch.svg)

## Installation

Download PiHole_mon.py and font file
```
wget https://raw.githubusercontent.com/Rob2n/PiHole_Monitor/main/PiHole_mon.py ; wget https://raw.githubusercontent.com/Rob2n/PiHole_Monitor/main/VCR_OSD_MONO_1.001.ttf
```
### Run on startup

Add a cron task by doing
```
crontab -e
```
and add the following line to the end
```
@reboot python3 /home/pi/PiHole_mon.py &
```
Every 30 seconds the screen refreshes the displayed data.

By pressing the button you can switch screens to display more info.
The different screens are:

* Screen 1 (Main)
  * Total blocked percentage
  * Total blocked count
* Screen 2
  * Total blocked count
  * Total number of queries
  * CPU temperature
* Screen 3
  * CPU usage
  * Memory in use/Total memory
  * Disk space used/Total disk space
