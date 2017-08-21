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

        self.isRunning = False
        return

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
