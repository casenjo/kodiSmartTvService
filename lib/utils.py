import xbmc
import xbmcaddon
import xbmcgui

__addOnId = u'service.smarttvservice'
__addOn = xbmcaddon.Addon(__addOnId)


def log(message, loglevel=xbmc.LOGNOTICE):
    xbmc.log(__addOnId + ": " + message, level=loglevel)

def getAddOnName():
    return __addOn.getAddonInfo('name')

def getSetting(settingId):
    return __addOn.getSetting(settingId)

def setSetting(settingId, settingValue):
    return __addOn.setSetting(settingId, settingValue)
