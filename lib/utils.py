import xbmc
import xbmcaddon
import xbmcgui

__addOnId = u'service.smarttvservice'
__addOn = xbmcaddon.Addon(__addOnId)


def log(message, loglevel=xbmc.LOGDEBUG):
    xbmc.log(__addOnId + ": " + message, level=loglevel)

def getAddOnName():
    return __addOn.getAddonInfo('name')

def getSetting(settingId):
    return __addOn.getSetting(settingId)

def setSetting(settingId, settingValue):
    return __addOn.setSetting(settingId, settingValue)

def notification(message, type=xbmcgui.NOTIFICATION_INFO):
    xbmcgui.Dialog().notification(getAddOnName(), message, type)

def notificationError(message):
    notification(message, xbmcgui.NOTIFICATION_ERROR)

def numberDialog(prompt):
    xbmcgui.Dialog().numeric(0, prompt)

def yesNoDialog(line1, line2='', line3=''):
    return xbmcgui.Dialog().yesno(getAddOnName(), line1, line2, line3)

def getString(stringId):
    return __addOn.getLocalizedString(stringId)
