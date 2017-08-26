import utils
from tv.tvfactory import TvFactory

class TvConnectionManager:

    def __init__(self):
        utils.log("TvConnectionManager starting")
        self.isRunning = True
        self.isConnected = False

        self.tvInput = utils.getTvInputSetting('tvInput')

        if not self.validateConfig():
            self.isRunning = False
            return

        # TODO: Change the TV brand so be retrieved from the settings
        self.tv = TvFactory().getTv("Sony")

        if self.tv.isConfigured():
            self.configureTvConnection()
        else:
            self.isConnected = self.tv.connect()

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

    # Configure TV connection
    def configureTvConnection(self):
        utils.log("Starting TV configuration")
        userWantsToConnect = self.tv.promptForConnection()

        if not userWantsToConnect:
            utils.log("User denied prompt, exiting")
            self.isRunning = False
            return

        self.isConnected = self.tv.configureConnection()

    def connectToTv(self):
        """

        :rtype: boolean
        """
        utils.log("Connecting to TV")
        return self.tv.connect()

    # Wake up our TV
    def wakeUpTv(self):
        utils.log("Waking TV up")
        if self.tvIsOff():
            self.tv.turnOn()

    # Change our TV to the input source in our config
    def setTvToKodiInput(self):
        if self.getTvInput() != self.tvInput:
            utils.log("Setting TV to Kodi input")
            self.tv.setInput(self.tvInput)

    # Get our TV's input source
    def getTvInput(self):
        return self.tv.getInput()

    def tvIsOff(self):
        return self.tv.isOff()

    def tvIsOn(self):
        return self.tv.isOn()

    def isTvSetToKodiInput(self):
        return self.getTvInput() == self.tvInput

    def turnOff(self):
        return self.tv.turnOff()
