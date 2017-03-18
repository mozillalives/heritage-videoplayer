# heritage-videoplayer
scripts and notes to support announcement video player setup on RaspberryPI at Heritage Baptist 

_loose notes for now, I'll cleanup when I'm done._

- Using PI Zero W, 16GB micro SD, USB and HDMI cords from AmazonBasics
- installed latest Raspbian lite
- setup ssh via usb (for initial config) via these instructions https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/
- changed hostname via these instructions https://www.dexterindustries.com/howto/change-the-hostname-of-your-pi/
- setup wifi via these instructions https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-occidentalis
- ran `update-locale LANG="en_US.UTF-8" LANGUAGE="en_US:en" LC_ALL="en_US.UTF-8"` to fix locale settings
- updated & upgraded installed packages

going to use this as basic premise https://github.com/timatron/videolooper-raspbian

- ran `sudo apt-get -y install omxplayer`
- moved announcements.sh to `/etc/init.d/announcements`
- made sure it was executable
- ran `touch /var/log/announcements.log`
- then ran `chown pi:pi /var/log/announcements.log`
- then ran `update-rc.d announcements defaults`

at this point, you should be able to restart the device and have it automatically start playing the video on boot
