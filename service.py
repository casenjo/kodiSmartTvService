import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import requests

from lib import braviarc

braviarc = braviarc.BraviaRC()
pin = u'5285'
braviarc.connect(pin, u'koditvwakeup', u'Kodi')

dialog = xbmcgui.Dialog()

xbmc.executebuiltin('ActivateScreensaver')

if braviarc.get_power_status() == u'standby':
    dialog.notification('test', 'turning on')
    braviarc.turn_on()
else:
    playing_content = braviarc.get_playing_info()
    if playing_content.get('title') != u'HDMI 1':
        braviarc.select_source('HDMI 1')
    # dialog.notification('test', 'turning off')
    # braviarc.turn_off()







