Kodi Smart TV Service
=====================
This is a work in progress project to have some control and automation
of your smart TV from within the Kodi media center application.

It runs as a Kodi service and monitors the TV and Kodi for activity,
turning off the TV after a certain length (in minutes) of inactivity.
It will also detect when Kodi is woken up and will turn the TV on (if
not already on) and switch to its Kodi input (if not already on it)

Right now it only works on Sony Bravia TVs. I'm not sure how far back
it will work, but any Bravia TV since 2015 should be compatible with
this service.


Installation
============

Install the files into a folder called `service.kodismarttvservice`
inside your Kodi installation's `addons` folder.

Not a simple installation (yet!), it will be published into the official
Kodi repo soon :)

Usage
=====
Go to
Kodi > Add-ons > My Add-ons > Services > Kodi Smart TV Service > Configure

And make sure that the TV's **IP address**, **MAC address** and
**Input** are selected.

**Do NOT change the PIN unless you've already configured the TV. When
you first enable the service you will set it.**

Enjoy!