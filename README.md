# Heritage Announcement Videoplayer
scripts and notes to support announcement video player setup on RaspberryPI at Heritage Baptist 

_loose notes for now, I'll cleanup when I'm done._

- Using PI Zero W, 16GB micro SD, USB and HDMI cords from AmazonBasics
- installed latest Raspbian lite
- setup ssh via usb (for initial config) via these instructions https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/
- changed the password of the `pi` user by running `passwd`
- changed hostname in `/etc/hostname` and in `/etc/hosts` (replace `raspberrypi` with your new hostname)
- setup wifi via these instructions https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-occidentalis
- ran `sudo dpkg-reconfigure locales` and in the wizard chose `en_US.UTF-8` and `en_US.UTF-8` again. I then `sudo update-locale LANG="en_US.UTF-8" LANGUAGE="en_US:en" LC_ALL="en_US.UTF-8"` to fix locale settings. (The second command might not have been necessary.)
- updated & upgraded installed packages by running `sudo apt-get update && sudo apt-get dist-upgrade -y`

going to use this as basic premise https://github.com/timatron/videolooper-raspbian
adapting a service [from this gist](https://gist.github.com/naholyr/4275302)

- downloaded `announcements.sh`, `hasher.py`, `sync_video.py` and `sample-settings.cfg` to `/home/pi`
- renamed `sample-settings.cfg` to `video-player-settings.cfg` and added actual settings
- ran `sudo apt-get -y install omxplayer`
- moved announcements.sh by running `sudo mv announcements.sh /etc/init.d/announcements`
- made sure it was executable by running `sudo chmod a+x /etc/init.d/announcements`
- ran `sudo touch /var/log/announcements.log`
- then ran `sudo chown pi:pi /var/log/announcements.log`
- then ran `sudo update-rc.d announcements defaults`

at this point, you should be able to restart the device and have it automatically start playing the video on boot
(provided you have the video in `/home/pi/videos/weekly-announcements.mp4`)

ran `sudo apt-get install python-pip -y`
ran `sudo pip install dropbox`

set the following crontab as root by running `sudo crontab -e`

    */15 * * * 0 /home/pi/sync_video.py -n 2>&1 | /usr/bin/logger -t sync_video

configured timezone by running `sudo dpkg-reconfigure tzdata`

ran `python sync_videos.py` script to set oauth token

# Dropbox
I created an app, enabled more users, created a special user account for dropbox, shared with new user, used oauth token from new user on PIs.

# TODO

- come up with maintenance plan
- make sure nothing is insecure in the default setup of raspbian
- setup automated update cron
- remote logging/status?
