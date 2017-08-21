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
        return  #debug
        utils.log("Requesting PIN from TV")
        self.connectToTv(self.tvPin)
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
