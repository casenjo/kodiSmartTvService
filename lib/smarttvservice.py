import utils


class SmartTvService:

    def __init__(self):
        utils.log("Smart TV Service starting")
        self.isRunning = True
        self.isConnected = False
        self.timeScreensaverActivated = 0
        self.TIME_TO_TV_SLEEP = (60 * int(utils.getSetting('timeUntilSleep')))  # Default setting is 5 minutes

        # start xbmc here
        # start TV connection manager

    def run(self):
        utils.log("Smart TV Service running")

