# Heritage Announcement Videoplayer
scripts and notes to support announcement video player setup on RaspberryPI at Heritage Baptist 

_loose notes for now, I'll cleanup when I'm done._

- Using PI Zero W, 16GB micro SD, USB and HDMI cords from AmazonBasics
- installed latest Raspbian lite
- setup ssh via usb (for initial config) via these instructions https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/
- changed hostname via these instructions https://www.dexterindustries.com/howto/change-the-hostname-of-your-pi/
- setup wifi via these instructions https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-occidentalis
- ran `sudo dpkg-reconfigure locales` then `sudo update-locale LANG="en_US.UTF-8" LANGUAGE="en_US:en" LC_ALL="en_US.UTF-8"` to fix locale settings
- updated & upgraded installed packages

going to use this as basic premise https://github.com/timatron/videolooper-raspbian
adapting a service [from this gist](https://gist.github.com/naholyr/4275302)

- ran `sudo apt-get -y install omxplayer`
- moved announcements.sh to `/etc/init.d/announcements`
- made sure it was executable
- ran `touch /var/log/announcements.log`
- then ran `chown pi:pi /var/log/announcements.log`
- then ran `update-rc.d announcements defaults`

at this point, you should be able to restart the device and have it automatically start playing the video on boot

ran `sudo apt-get install python-pip`
ran `sudo pip install dropbox`
saved `sync_videos.py` to pi home directory

set the following crontab as root by running `sudo crontab -e`

    */15 9,10,11 * * 0 /home/pi/sync_video.py -n 2>&1 | /usr/bin/logger -t sync_video
    */15 17,18 * * 0 /home/pi/sync_video.py -n 2>&1 | /usr/bin/logger -t sync_video
    */15 18 * * 3 /home/pi/sync_video.py -n 2>&1 | /usr/bin/logger -t sync_video

configured timezone by running `sudo dpkg-reconfigure tzdata`

placed a copy of the config file in the pi home directory and named it `.dropbox-auth`

ran the `sync_videos.py` script to set oauth token

# Dropbox
I created an app, enabled more users, created a special user account for dropbox, shared with new user, used oauth token from new user on PIs.

# TODO

- come up with maintenance plan
- make sure nothing is insecure in the default setup of raspbian
- setup automated update cron
- remote logging/status?
- download new file to temp file, then move into place when done
