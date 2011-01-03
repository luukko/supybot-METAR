#vim: set fileencoding=utf8
###
# METAR supybot plugin
#
# written on Dec 2010 by louk
# published under 'do whatever you want'-license
###

from supybot.commands import *
import supybot.callbacks as callbacks

import re, urllib
from metar import Metar
from datetime import datetime

BASE_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations"

class ReportNotFoundError(Exception):
    """This exception is thrown if no valid METAR report is found by get_report."""
    def __init__(self, url, station):
        self.url = url
        self.station = station
    def __str__(self):
        print "METAR report for %s not found at %s" % (self.station, self.url)

def get_report(station):
    """Fetch a METAR report for given station code via http."""
    url = "%s/%s.TXT" % (BASE_URL, station)
    urlh = urllib.urlopen(url)
    for line in urlh:
        if line.startswith(station):
            return line.strip()
    raise ReportNotFoundError(url, station)

def format_report(report, format_level):
    """Format a human-readable report from given raw METAR report.

    Format level: <=0 - raw
                  1 - short
                  2 - standard
                  >=3 - full
    """
    if format_level == 0:
        return report
    obs = Metar.Metar(report)
    # Create useful representation of observation time; if the date is the current day,
    # only print the time
    timeobj = obs.time
    if timeobj.date() == datetime.now().date():
        timestring = timeobj.strftime("%H:%M")
    else:
        timestring = timeobj.strftime("%Y-%m-%d %H:%M")
    # Create useful representation of wind conditions
    if obs.wind_speed == None:
        windstring = None
    elif obs.wind_speed.value() == 0.0:
        windstring = "calm"
    else:
        wind_speed = "%.1f m/s" % obs.wind_speed.value("mps")
        if not obs.wind_dir:
            windstring = "variable at %s" % wind_speed
        elif obs.wind_dir_from:
            windstring = "%s to %s at %s" % \
                             (obs.wind_dir_from.compass(), obs.wind_dir_to.compass(), wind_speed)
        else:
            windstring = "%s at %s" % (obs.wind_dir.compass(), wind_speed)
        if obs.wind_gust:
            windstring += ", gusting to %.1f m/s" % obs.wind_gust.value("mps")
    # Compile all observation data in a dictionary for easy string formatting
    data = { "station": obs.station_id,
             "time": timestring,
             "temp": str(obs.temp.value("C"))+" °C",
             "pressure": str(obs.press.value("mb"))+" mbar",
             "wind": windstring,
             "weather": obs.present_weather(),
             "dewpt" : str(obs.dewpt.value("C"))+" °C",
             "visibility" : obs.visibility(units="m"),
             "sky": obs.sky_conditions(),
             "remarks": obs.remarks(),
             "precipitation": obs.precip_1hr.string("cm") if obs.precip_1hr else None}
    # Compile format string based on format level
    format_string = "%(station)s at %(time)s: %(temp)s"
    if data["weather"]:
        format_string += ", %(weather)s"
    if format_level >= 2:
        if data["pressure"]:
            format_string += ", pressure %(pressure)s"
        if data["wind"]:
            format_string += ", wind %(wind)s"
        if data["dewpt"]:
            format_string += ", dew point %(dewpt)s"
    if format_level >= 3:
        if data["visibility"]:
            format_string += ", visibility %(visibility)s"
        if data["sky"]:
            format_string += ", %(sky)s"
        if data["precipitation"]:
            format_string += ", precipitation %(precipitation)s"
        if data["remarks"]:
            format_string += ", remarks: %(remarks)s"
    return format_string % data

class METAR(callbacks.Plugin):
    def metar(self, irc, msg, args, reptype, station):
        """[raw|short|standard|full] <station code>
        Retrieves current weather conditions for a given METAR observation station.

        A comprehensive list of station codes: http://www.rap.ucar.edu/weather/surface/stations.txt"""
        # sanitize user input, allows only alphanumerical chars
        station = re.sub('[^\w]', '', station)
        # convert station to uppercase
        station = station.upper()
        # fetch METAR report
        report = get_report(station)
        # parse reptype
        if reptype == "short":
            format_level = 1
        elif not reptype or reptype == "standard":
            format_level = 2
        elif reptype == "full":
            format_level = 3
        else:
            format_level = 0
        # format the report
        output = format_report(report, format_level)
        irc.reply(output)

    # at last the wrapper..
    metar = wrap(metar, [optional(("literal", ("raw", "short", "standard", "full"), 'argument parse error')), 'something'])
