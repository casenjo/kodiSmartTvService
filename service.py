import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
import requests
from lib import braviarc

serviceName = u"Bravia TV Service"

serviceClientId = u'koditvwakeup'
serviceNickname = u'Kodi'
serviceTvPin = u'PIN_HERE'

tvIp = u'TV_IP_HERE'
tvMac = u'TV_MAC_HERE'

# Extend the xbmc.Monitor class to do our bidding
class TvMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.log("2 " + serviceName + " (TV Monitor): starting", level=xbmc.LOGDEBUG)
        self.dialog = xbmcgui.Dialog()
        self.braviarc = braviarc.BraviaRC(tvIp, tvMac)
        self.pin = serviceTvPin
        self.braviarc.connect(self.pin, serviceClientId, serviceNickname)
        self.timeScreensaverActivated = 0
        self.TIME_TO_TV_SLEEP = (60 * 5)

    def onScreensaverDeactivated(self):
        xbmc.log("3 " + serviceName + " (TV Monitor): screensaver deactivated", level=xbmc.LOGDEBUG)
        # section wakeup
        if self.tvIsOff():
            self.dialog.notification(serviceName, 'Turning on')
            self.braviarc.turn_on()
            xbmc.sleep(2000);
        # section wakeup

        # section setToKodiSource
        playing_content = self.braviarc.get_playing_info()
        if playing_content.get('title') != u'HDMI 1':
            self.braviarc.select_source('HDMI 1')
        # section setToKodiSource

    def tvIsOff(self):
        return self.braviarc.get_power_status() == u'standby'

    def tvIsOn(self):
        return self.braviarc.get_power_status() == u'active'

    def onScreensaverActivated(self):
        xbmc.log("4 " + serviceName + " (TV Monitor): screensaver activated", level=xbmc.LOGDEBUG)
        self.timeScreensaverActivated = time.time()

    def checkIfTimeToSleep(self):
        if self.tvIsOn() and xbmc.getCondVisibility("System.ScreenSaverActive"):
            xbmc.log("5 " + serviceName + " (TV Monitor): Going to sleep", level=xbmc.LOGDEBUG)
            currentTime = time.time()
            playing_content = self.braviarc.get_playing_info()
            if playing_content.get('title') == u'HDMI 1' and ((currentTime - self.timeScreensaverActivated) > self.TIME_TO_TV_SLEEP):
                self.braviarc.turn_off()

# Service entry point
if __name__ == '__main__':
    xbmc.log("1 " + serviceName + ": Starting", level=xbmc.LOGDEBUG)

    tvMonitor = TvMonitor()

    # Toggle screensaver for faster debugging
    xbmc.executebuiltin('ActivateScreensaver')

    while not tvMonitor.abortRequested():
        # Sleep/wait for abort for 2 seconds
        if tvMonitor.waitForAbort(2):
            # Abort was requested while waiting. We should exit
            break
        tvMonitor.checkIfTimeToSleep()
