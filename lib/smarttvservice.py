import utils
from tvconnectionmanager import TvConnectionManager
import xbmc

class SmartTvService:

    def __init__(self):
        utils.log("Smart TV Service starting")
        self.tvConnectionManager = TvConnectionManager()
        self.monitor = xbmc.Monitor(self.tvConnectionManager)

    def run(self):
        utils.log("Smart TV Service running")

        while not self.monitor.abortRequested() and self.tvConnectionManager.isRunning:
            # Sleep/wait for abort for 2 seconds
            if self.monitor.waitForAbort(2):
                # Abort was requested while waiting. We should exit
                utils.log("Kodi abort detected, stopping service execution")
                break
            self.tick()

    def tick(self):
        #         if tvConnectionManager.isConnected:
        #             tvMonitor.checkIfTimeToSleep()
        utils.log("Tick")
