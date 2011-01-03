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

nuteater = supybot.Author("Perttu Luukko", "Nuteater")
louk = supybot.Author("louk")

__version__ = "0.2"
__author__ = nuteater
__contributors__ = { louk: ["original version"] }
__url__ = 'https://github.com/nuteater/supybot-METAR/'

import config
import plugin
reload(plugin) # In case we're being reloaded.
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    import test

Class = plugin.METAR
configure = config.configure
