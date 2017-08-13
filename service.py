import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
import requests
from lib import braviarc

name = u"Bravia TV Wakeup Service"

# Extend the xbmc.Monitor class to do our bidding
class TvWakeupMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.log("2 " + name + " (TV Wakeup Monitor): starting", level=xbmc.LOGDEBUG)
        self.dialog = xbmcgui.Dialog()
        self.braviarc = braviarc.BraviaRC(u'TV_IP_HERE', u'TV_MAC_HERE')
        self.pin = u'5285'
        self.braviarc.connect(self.pin, u'koditvwakeup', u'Kodi')

    def onScreensaverDeactivated(self):
        xbmc.log("3 " + name + " (TV Wakeup Monitor): screensaver deactivated", level=xbmc.LOGDEBUG)
        if self.braviarc.get_power_status() == u'standby':
            self.dialog.notification('test', 'turning on')
            self.braviarc.turn_on()
            xbmc.sleep(2000);

        playing_content = self.braviarc.get_playing_info()
        if playing_content.get('title') != u'HDMI 1':
            self.braviarc.select_source('HDMI 1')

# Service entry point
if __name__ == '__main__':
    xbmc.log("1 " + name + ": Starting", level=xbmc.LOGDEBUG)

    tvWakeupMonitor = TvWakeupMonitor()

    # Toggle screensaver for faster debugging
    xbmc.executebuiltin('ActivateScreensaver')

    while not tvWakeupMonitor.abortRequested():
        # Sleep/wait for abort for 2 seconds
        if tvWakeupMonitor.waitForAbort(2):
            # Abort was requested while waiting. We should exit
            break
