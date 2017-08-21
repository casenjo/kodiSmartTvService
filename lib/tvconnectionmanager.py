import utils
import braviarc

class TvConnectionManager():

    def __init__(self):
        utils.log("TvConnectionManager starting")
        self.isRunning = True
        self.isConnected = False

        self.tvIp = utils.getSetting('tvIpAddress')
        self.tvMacAddress = utils.getSetting('tvMacAddress')
        self.tvPin = utils.getSetting('tvPin')
        self.tvInput = utils.getTvInputSetting('tvInput')

        if not self.validateConfig():
            self.isRunning = False
            return

        # TODO: This needs to be handled by a factory in order to use a generic TV instead of a specific one
        # self.braviarc = braviarc.BraviaRC(self.tvIp, self.tvMacAddress)

        if self.pinIsDefault():
            self.configureTvConnection()
        else:
            self.isConnected = self.connectToTv(self.tvPin)

        # debug only
        self.isRunning = False
        return
        # debug only

    # Check configuration to make sure we can make an initial connection to the TV
    def validateConfig(self):
        utils.log("Checking configuration")
        if self.tvIp == '':
            utils.log("Configuration invalid, TV IP is missing")
            utils.notificationError(utils.getString(30016))
            return False
        if self.tvMacAddress == '':
            utils.log("Configuration invalid, TV MAC is missing")
            utils.notificationError(utils.getString(30017))
            return False
        if self.tvInput == '':
            utils.log("Configuration invalid, TV Input must be selected")
            utils.notificationError(utils.getString(30018))
            return False
        utils.log("Configuration validated")
        return True

    # Check configured PIN isn't the default
    def pinIsDefault(self):
        return self.tvPin == "0000"

    # Configure TV connection
    # TODO: Clean up code inside to be independent of Bravia-specific functions
    def configureTvConnection(self):
        utils.log("Default PIN detected, starting configuration flow")
        userWantsToConnect = utils.yesNoDialog(utils.getString(30011), utils.getString(30012), utils.getString(30013))

        if not userWantsToConnect:
            utils.log("User denied prompt, exiting")
            self.isRunning = False
            return

        utils.log("Requesting PIN from TV")
        self.connectToTv(self.tvPin)

        pinFromTv = self.getPinFromUserPrompt()
        if pinFromTv is False:
            return

        utils.log("PIN " + pinFromTv + " entered")

        self.connectToTv(pinFromTv)

        if not self.braviarc.is_connected():
            utils.log("PIN incorrect, exiting")
            utils.notificationError(utils.getString(30015))
            self.isRunning = False
            return
        else:
            utils.log("PIN correct, saving to plugin settings")
            utils.setSetting('tvPin', pinFromTv)
            self.tvPin = utils.getSetting('tvPin')
            utils.log("New PIN is " + self.tvPin)
            self.isConnected = self.connectToTv(self.tvPin)

    # TODO: Clean up code inside to be independent of Bravia-specific functions and use a generic TV object
    def connectToTv(self, pin):
        """

        :rtype: boolean
        """
        utils.log("Connecting to TV")
        if not self.validatePin(pin):
            return False

        return self.braviarc.connect(pin, utils.addOnTvClientId, utils.getAddOnName())

    # TODO: This should be inside a Bravia-specific TV class
    def validatePin(self, pinFromTv=''):
        return pinFromTv != '' and pinFromTv.isdigit() and len(pinFromTv) == 4

    # Get a pin from the user when setting up the TV
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def getPinFromUserPrompt(self):
        pinFromTv = ''

        while not self.validatePin(pinFromTv):
            pinFromTv = utils.numberDialog(utils.getString(30014))
            if not self.validatePin(pinFromTv):
                userWantsToTryAgain = utils.yesNoDialog('PIN incorrect, it needs to be exactly 4 digits.', 'Try again?')
                if not userWantsToTryAgain:
                    break

        if pinFromTv == '':
            return False
        else:
            return pinFromTv

    # Wake up our TV
    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def wakeUpTv(self):
        utils.log("Waking TV up")
        if self.tvIsOff():
            self.braviarc.turn_on()

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

    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def tvIsOff(self):
        return self.braviarc.get_power_status() == u'standby'

    # TODO: This is too specific to Bravia TVs, part of it should be moved to a Bravia specific class and use a generic getTvSource method to get it instead
    def tvIsOn(self):
        return self.braviarc.get_power_status() == u'active'

    def isTvSetToKodiInput(self):
        return self.getTvInput() == self.tvInput

    def turnOff(self):
        return self.braviarc.turn_off()
