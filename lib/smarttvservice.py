import utils
from tvconnectionmanager import TvConnectionManager
from kodimonitor import KodiMonitor


class SmartTvService:

    def __init__(self):
        utils.log("Smart TV Service starting")
        # self.tvConnectionManager = TvConnectionManager()
        # self.monitor = KodiMonitor(self.tvConnectionManager)

        tv = TvFactory().getTv("Sony")
        utils.log(tv.getName())

    def run(self):
        utils.log("Smart TV Service running")

        # while not self.monitor.abortRequested() and self.tvConnectionManager.isRunning:
        #     # Sleep/wait for abort for 2 seconds
        #     if self.monitor.waitForAbort(2):
        #         # Abort was requested while waiting. We should exit
        #         utils.log("Kodi abort detected, stopping service execution")
        #         break
        #     self.tick()

    def tick(self):
        if self.tvConnectionManager.isConnected:
            self.monitor.checkIfTimeToSleep()



class TvSony: # implements TV contract

    def getName(self):
        return "Sony TV here"

class TvFactory:

    def __init__(self):
        self.availableTvs = dict(Sony=TvSony)

    def getTv(self, tv=None):
        return self.availableTvs[tv]()
