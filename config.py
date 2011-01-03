# METAR supybot plugin
#
# written originally on Dec 2010 by louk
# improved by nuteater
# published under 'do whatever you want'-license

import supybot.conf as conf

def configure(advanced):
    conf.registerPlugin('METAR', True)

METAR = conf.registerPlugin('METAR')
