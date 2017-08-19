import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
import requests
from lib import braviarc

serviceName = u"Kodi Smart TV Service"
serviceId = u"service.smarttvservice"
serviceClientId = u'kodismarttvservice'
serviceNickname = u'Kodi Smart TV Service'

# Extend the xbmc.Monitor class to do our bidding
class TvMonitor(xbmc.Monitor):

    def __init__(self):
        xbmc.log(serviceName + " (TV Monitor): Starting", level=xbmc.LOGDEBUG)

        self.addon = xbmcaddon.Addon(serviceId)
        self.dialog = xbmcgui.Dialog()

        self.isRunning = True
        self.isConnected = False
        self.timeScreensaverActivated = 0
        self.tvIp = self.addon.getSetting('tvIpAddress')
        self.tvMacAddress = self.addon.getSetting('tvMacAddress')
        self.tvPin = self.addon.getSetting('tvPin')
        self.tvInput = self.getTvInputSetting()
        self.TIME_TO_TV_SLEEP = (60 * int(self.addon.getSetting('timeUntilSleep')))  # Default setting is 5 minutes

        if not self.configIsValid():
            self.isRunning = False
            return

        self.braviarc = braviarc.BraviaRC(self.tvIp, self.tvMacAddress)

        if self.pinIsDefault():
            self.configureTvConnection()
        else:
            self.connectToTv()

    def getTvInputSetting(self):
        input = self.addon.getSetting('tvInput')
        # 0 => HDMI 1, 1 => HDMI 2, etc
        return {
            '0': 'HDMI 1',
            '1': 'HDMI 2',
            '2': 'HDMI 3',
            '3': 'HDMI 4'
        }.get(input, '')  # '' is default if input not found

    def connectToTv(self):
        xbmc.log(serviceName + " (TV Monitor): Connecting to TV.", level=xbmc.LOGDEBUG)
        self.braviarc.connect(self.tvPin, serviceClientId, serviceNickname)
        self.isConnected = True

    # Configure TV connection
    def configureTvConnection(self):
        xbmc.log(serviceName + " (TV Monitor): Default PIN detected, starting configuration flow", level=xbmc.LOGDEBUG)
        userWantsToConnect = self.dialog.yesno(serviceName,
                                               'Plugin not connected to the TV. Do you want to connect to it?',
                                               'If yes, be aware that the dialog on the TV might be large and will not let you see the interface to input the PIN.',
                                               'You can use your keyboard to type the code and then press Enter :)')

        if not userWantsToConnect:
            xbmc.log(serviceName + " (TV Monitor): User denied prompt, exiting.", level=xbmc.LOGDEBUG)
            self.isRunning = False
            return

        xbmc.log(serviceName + " (TV Monitor): Requesting PIN from TV.", level=xbmc.LOGDEBUG)
        self.braviarc.connect(self.tvPin, serviceClientId, serviceNickname)
        pinFromTv = self.dialog.numeric(0, 'Enter PIN from TV')
        xbmc.log(serviceName + " (TV Monitor): PIN " + pinFromTv + " entered", level=xbmc.LOGDEBUG)

        self.braviarc.connect(pinFromTv, serviceClientId, serviceNickname)

        if not self.braviarc.is_connected():
            xbmc.log(serviceName + " (TV Monitor): PIN incorrect, exiting.", level=xbmc.LOGDEBUG)
            self.dialog.notification(serviceName, 'PIN incorrect, unable to connect', xbmcgui.NOTIFICATION_ERROR)
            self.isRunning = False
            return
        else:
            xbmc.log(serviceName + " (TV Monitor): PIN correct, saving to settings.", level=xbmc.LOGDEBUG)
            self.addon.setSetting('tvPin', pinFromTv)
            self.tvPin = self.addon.getSetting('tvPin')
            xbmc.log(serviceName + " (TV Monitor): New PIN is " + self.tvPin, level=xbmc.LOGDEBUG)
            self.connectToTv()

    # Check configured PIN isn't the default
    def pinIsDefault(self):
        return self.tvPin == "0000"

    # Check configuration to make sure we can make an initial connection to the TV
    def configIsValid(self):
        xbmc.log(serviceName + " (TV Monitor): Checking configuration", level=xbmc.LOGDEBUG)
        if self.tvIp == '':
            xbmc.log(serviceName + " (TV Monitor): Configuration failed, TV IP is missing", level=xbmc.LOGDEBUG)
            self.dialog.notification(serviceName, 'TV IP address not configured', xbmcgui.NOTIFICATION_ERROR)
            return False
        if self.tvMacAddress == '':
            xbmc.log(serviceName + " (TV Monitor): Configuration failed, TV MAC is missing", level=xbmc.LOGDEBUG)
            self.dialog.notification(serviceName, 'TV MAC address not configured', xbmcgui.NOTIFICATION_ERROR)
            return False
        if self.tvInput == '':
            xbmc.log(serviceName + " (TV Monitor): Configuration failed, TV Input must be selected", level=xbmc.LOGDEBUG)
            self.dialog.notification(serviceName, 'TV Input must be selected', xbmcgui.NOTIFICATION_ERROR)
            return False
        xbmc.log(serviceName + " (TV Monitor): Configuration validated!", level=xbmc.LOGDEBUG)
        return True

    def onScreensaverDeactivated(self):
        xbmc.log(serviceName + " (TV Monitor): Screensaver deactivated", level=xbmc.LOGDEBUG)
        self.wakeUpTv()
        self.setTvToKodiInput()

    # Wake up our TV
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def wakeUpTv(self):
        xbmc.log(serviceName + " (TV Monitor): Waking TV up", level=xbmc.LOGDEBUG)
        if self.tvIsOff():
            self.braviarc.turn_on()
            xbmc.sleep(2000)  # Let the TV turn on before ending the method's execution

    # Change our TV to the input source in our config
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def setTvToKodiInput(self):
        if self.getTvInput() != self.tvInput:
            xbmc.log(serviceName + " (TV Monitor): Setting TV to Kodi input", level=xbmc.LOGDEBUG)
            self.braviarc.select_source(self.tvInput)

    # Get our TV's input source
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def getTvInput(self):
        playing_content = self.braviarc.get_playing_info()
        return playing_content.get('title')

    def tvIsOff(self):
        return self.braviarc.get_power_status() == u'standby'

    def tvIsOn(self):
        return self.braviarc.get_power_status() == u'active'

    def onScreensaverActivated(self):
        xbmc.log(serviceName + " (TV Monitor): screensaver activated", level=xbmc.LOGDEBUG)
        self.resetScreensaverActivationTime()

    def resetScreensaverActivationTime(self):
        self.timeScreensaverActivated = int(time.time())

    def isTvSetToKodiInput(self):
        return self.getTvInput() == self.tvInput

    def isTimeToSleep(self):
        currentTime = int(time.time())
        return (currentTime - self.timeScreensaverActivated) > self.TIME_TO_TV_SLEEP

    def checkIfTimeToSleep(self):
        xbmc.log(serviceName + " (TV Monitor): Checking if going to sleep", level=xbmc.LOGDEBUG)
        if self.tvIsOff():
            self.resetScreensaverActivationTime()
        if xbmc.getCondVisibility("System.ScreenSaverActive") and self.tvIsOn():

            if self.isTvSetToKodiInput() and self.isTimeToSleep():
                xbmc.log(serviceName + " (TV Monitor): Input is " + self.tvInput + " and its past our bedtime, going to sleep", level=xbmc.LOGDEBUG)
                xbmc.log(serviceName + " (TV Monitor): TURNING OFF NOW", level=xbmc.LOGDEBUG)
                # self.braviarc.turn_off()

            # Reset the screensaver activated time because we're using another input and if
            # we switch inputs manually afterwards, the TV will turn off almost instantly lol
            if not self.isTvSetToKodiInput():
                xbmc.log(serviceName + " (TV Monitor): Input is not " + self.tvInput + ", resetting timer", level=xbmc.LOGDEBUG)
                self.resetScreensaverActivationTime()


# Service entry point
if __name__ == '__main__':
    xbmc.log(serviceName + ": Starting", level=xbmc.LOGDEBUG)

    tvMonitor = TvMonitor()

    # Toggle screensaver for faster debugging
    xbmc.executebuiltin('ActivateScreensaver')

    while not tvMonitor.abortRequested() and tvMonitor.isRunning:
        # Sleep/wait for abort for 2 seconds
        if tvMonitor.waitForAbort(2):
            # Abort was requested while waiting. We should exit
            xbmc.log("ABORTING", level=xbmc.LOGDEBUG)
            break
        if tvMonitor.isConnected:
            tvMonitor.checkIfTimeToSleep()