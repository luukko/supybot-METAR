###
# METAR supybot plugin
#
# written on Dec 2010 by louk
# published under 'do whatever you want'-license
###

import supybot.conf as conf

def configure(advanced):
    conf.registerPlugin('METAR', True)

METAR = conf.registerPlugin('METAR')
