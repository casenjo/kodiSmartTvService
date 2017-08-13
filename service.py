import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
import requests

name = u"Bravia TV Wakeup Service"


class TvWakeupMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.log("2 " + name + " (TV Wakeup Monitor): starting", level=xbmc.LOGDEBUG)

    def onScreensaverDeactivated(self):
        xbmc.log("3 " + name + " (TV Wakeup Monitor): screensaver deactivated", level=xbmc.LOGDEBUG)
        xbmc.log(name + " (TV Wakeup Monitor): DO CHECKS FOR TV STATUS HERE", level=xbmc.LOGDEBUG)

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
