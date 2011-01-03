# METAR supybot plugin
#
# written originally on Dec 2010 by louk
# improved by nuteater
# published under 'do whatever you want'-license

"""
wrapper for METAR data fetcher and parser
"""

import supybot
import supybot.world as world

__version__ = "0.1"
__author__ = "louk"
__contributors__ = {}
__url__ = '' # 'github/anza/supybot-metar'

import config
import plugin
reload(plugin) # In case we're being reloaded.
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    import test

Class = plugin.METAR
configure = config.configure
