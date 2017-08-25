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
