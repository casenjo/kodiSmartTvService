from ..braviarc import BraviaRC


class TvSony: # implements TV contract

    def __init__(self, ipAddress='', macAddress=''):
        self.ipAddress = ipAddress
        self.macAddress = macAddress
        self.tv = BraviaRC(self.tvIp, self.tvMacAddress)

    def getName(self):
        return "Sony TV here"

    def getInput(self):
        playing_content = self.tv.get_playing_info()
        return playing_content.get('title')

    def isOff(self):
        return self.tv.get_power_status() == u'standby'

    def turnOn(self):
        self.tv.turn_on()

    def isOn(self):
        return self.tv.get_power_status() == u'active'