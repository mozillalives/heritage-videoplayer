#!/usr/bin/env python
import os, datetime, subprocess, ConfigParser, sys, urllib2, socket, json
import dropbox

CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.dropbox-oauth')

cfg = ConfigParser.ConfigParser()
cfg.read(CONFIG_FILE)
APP_KEY = cfg.get('general', 'app_key')
APP_SECRET = cfg.get('general', 'app_secret')
SLACK_URL = cfg.get('general', 'slack_url')
try:
    OAUTH_TOKEN = cfg.get('general', 'oauth_token')
except ConfigParser.NoOptionError:
    if '-n' in sys.argv:
        raise SystemError("No OAuth token, exiting")

    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    authorize_url = auth_flow.start()
    print "1. Go to: " + authorize_url
    print "2. Click \"Allow\" (you might have to log in first)."
    print "3. Copy the authorization code."
    auth_code = raw_input("Enter the authorization code here: ").strip()

    oauth_result = auth_flow.finish(auth_code)
    OAUTH_TOKEN = oauth_result.access_token
    cfg.set('general', 'oauth_token', OAUTH_TOKEN)
    with open(CONFIG_FILE, 'wb') as configfile:
        cfg.write(configfile)


def main():
    dbx = dropbox.Dropbox(OAUTH_TOKEN)

    lfilename = "/home/pi/videos/weekly-announcements.mp4"
    dfilename = "/announcements/weekly-announcements.mp4"
    lmod = datetime.datetime.utcfromtimestamp(os.path.getmtime(lfilename))
    dmod = dbx.files_get_metadata(dfilename).server_modified

    if dmod <= lmod:
        return False
    
    dbx.files_download_to_file(lfilename, dfilename)
    subprocess.call(["chown", "pi:pi", lfilename])
    subprocess.call(["service", "announcements", "restart"])
    return True


def send_notice(msg):
    req = urllib2.Request(SLACK_URL, headers={"Content-Type": "application/json"},
                          data=json.dumps({'text' : msg}))
    urllib2.urlopen(req)


if __name__ == '__main__':
    try:
        if main():
            send_notice("{} downloaded new file".format(socket.gethostname()))
    except Exception as e:
        send_notice("{} had a problem: {}".format(socket.gethostname(), e))
