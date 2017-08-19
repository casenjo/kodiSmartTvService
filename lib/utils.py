import xbmc
import xbmcaddon
import xbmcgui

__addOnId = u'service.smarttvservice'
__addOn = xbmcaddon.Addon(__addOnId)


def log(message, loglevel=xbmc.LOGNOTICE):
    xbmc.log(__addOnId + ": " + message, level=loglevel)
