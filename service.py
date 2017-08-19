import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
from lib import braviarc, utils

serviceName = u"Kodi Smart TV Service"
serviceId = u"service.smarttvservice"
serviceClientId = u'kodismarttvservice'
serviceNickname = u'Kodi Smart TV Service'

# Extend the xbmc.Monitor class to do our bidding
class TvMonitor(xbmc.Monitor):

    def __init__(self):
        utils.log("Monitor starting")

        self.addon = xbmcaddon.Addon(serviceId)
        self.dialog = xbmcgui.Dialog()

        self.isRunning = True
        self.isConnected = False
        self.timeScreensaverActivated = 0
        self.tvIp = self.addon.getSetting('tvIpAddress')
        self.tvMacAddress = self.addon.getSetting('tvMacAddress')
        self.tvPin = self.addon.getSetting('tvPin')
        self.tvInput = self.getTvInputSetting()
        self.TIME_TO_TV_SLEEP = (1 * int(self.addon.getSetting('timeUntilSleep')))  # Default setting is 5 minutes

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
        utils.log("Connecting to TV")
        self.braviarc.connect(self.tvPin, serviceClientId, serviceNickname)
        self.isConnected = True

    # Configure TV connection
    def configureTvConnection(self):
        utils.log("Default PIN detected, starting configuration flow")
        userWantsToConnect = self.dialog.yesno(serviceName,
                                               'Plugin not connected to the TV. Do you want to connect to it?',
                                               'If yes, be aware that the dialog on the TV might be large and will not let you see the interface to input the PIN.',
                                               'You can use your keyboard to type the code and then press Enter :)')

        if not userWantsToConnect:
            utils.log("User denied prompt, exiting")
            self.isRunning = False
            return

        utils.log("Requesting PIN from TV")
        self.braviarc.connect(self.tvPin, serviceClientId, serviceNickname)
        pinFromTv = self.dialog.numeric(0, 'Enter PIN from TV')
        utils.log("PIN " + pinFromTv + " entered")

        self.braviarc.connect(pinFromTv, serviceClientId, serviceNickname)

        if not self.braviarc.is_connected():
            utils.log("PIN incorrect, exiting")
            self.dialog.notification(serviceName, 'PIN incorrect, unable to connect', xbmcgui.NOTIFICATION_ERROR)
            self.isRunning = False
            return
        else:
            utils.log("PIN correct, saving to plugin settings")
            self.addon.setSetting('tvPin', pinFromTv)
            self.tvPin = self.addon.getSetting('tvPin')
            utils.log("New PIN is " + self.tvPin)
            self.connectToTv()

    # Check configured PIN isn't the default
    def pinIsDefault(self):
        return self.tvPin == "0000"

    # Check configuration to make sure we can make an initial connection to the TV
    def configIsValid(self):
        utils.log("Checking configuration")
        if self.tvIp == '':
            utils.log("Configuration failed, TV IP is missing")
            self.dialog.notification(serviceName, 'TV IP address not configured', xbmcgui.NOTIFICATION_ERROR)
            return False
        if self.tvMacAddress == '':
            utils.log("Configuration failed, TV MAC is missing")
            self.dialog.notification(serviceName, 'TV MAC address not configured', xbmcgui.NOTIFICATION_ERROR)
            return False
        if self.tvInput == '':
            utils.log("Configuration failed, TV Input must be selected")
            self.dialog.notification(serviceName, 'TV Input must be selected', xbmcgui.NOTIFICATION_ERROR)
            return False
        utils.log("Configuration validated")
        return True

    def onScreensaverDeactivated(self):
        utils.log("Screensaver deactivated")
        self.wakeUpTv()
        self.setTvToKodiInput()

    # Wake up our TV
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def wakeUpTv(self):
        utils.log("Waking TV up")
        if self.tvIsOff():
            self.braviarc.turn_on()
            xbmc.sleep(2000)  # Let the TV turn on before ending the method's execution

    # Change our TV to the input source in our config
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def setTvToKodiInput(self):
        if self.getTvInput() != self.tvInput:
            utils.log("Setting TV to Kodi input")
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
        utils.log("Screensaver activated")
        self.resetScreensaverActivationTime()

    def resetScreensaverActivationTime(self):
        self.timeScreensaverActivated = int(time.time())

    def isTvSetToKodiInput(self):
        return self.getTvInput() == self.tvInput

    def isTimeToSleep(self):
        currentTime = int(time.time())
        return (currentTime - self.timeScreensaverActivated) > self.TIME_TO_TV_SLEEP

    def checkIfTimeToSleep(self):
        utils.log("Checking if going to sleep")
        if self.tvIsOff():
            self.resetScreensaverActivationTime()
        if xbmc.getCondVisibility("System.ScreenSaverActive") and self.tvIsOn():

            if self.isTvSetToKodiInput() and self.isTimeToSleep():
                utils.log("Input is " + self.tvInput + " and its past our bedtime, going to sleep")
                utils.log("TURNING TV OFF NOW")
                # self.braviarc.turn_off()

            # Reset the screensaver activated time because we're using another input and if
            # we switch inputs manually afterwards, the TV will turn off almost instantly lol
            if not self.isTvSetToKodiInput():
                utils.log("Input is not " + self.tvInput + ", resetting screensaver timer")
                self.resetScreensaverActivationTime()


# Service entry point
if __name__ == '__main__':

    tvMonitor = TvMonitor()

    # Toggle screensaver for faster debugging
    xbmc.executebuiltin('ActivateScreensaver')

    while not tvMonitor.abortRequested() and tvMonitor.isRunning:
        # Sleep/wait for abort for 2 seconds
        if tvMonitor.waitForAbort(2):
            # Abort was requested while waiting. We should exit
            utils.log("ABORTING")
            break
        if tvMonitor.isConnected:
            tvMonitor.checkIfTimeToSleep()