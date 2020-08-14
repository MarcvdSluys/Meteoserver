# Meteoserver #

A Python module to obtain and read Dutch weather data from Meteoserver.nl.  The code is being developped by
[Marc van der Sluys](http://han.vandersluys.nl/en/) of the department of Sustainable energy of the HAN
University of Applied Sciences in Arnhem, the Netherlands.


## Installation ##

This package can be installed using `pip install meteoserver`.  This should automatically install the dependency
packages `pandas` and `requests`, if they haven't been installed already.
If you are installing by hand, ensure that these packages are installed as well.

You will need to obtain a (free) account and API key at [Meteoserver.nl](https://meteoserver.nl/) to download
data from the Meteoserver API.


## Example use ##

```python
"""Example Python script using the Meteoserver module."""

import meteoserver as meteo

myKey = 'a123456789'    # My Meteoserver API key - put your OWN key here!
myLocation = 'De Bilt'  # My location

# Print some help:
meteo.print_help_zonactueel()

# Read a Meteoserver JSON file from disc:
# current, forecast = meteo.read_json_file_zon('ZonActueel.json')

# Get Meteoserver Sun data from the server for the given location (and key):
current, forecast = meteo.read_json_url_zon(myKey, myLocation)

# Print the current-weather and forecast dataframes:
print("\nCurrent Sun/weather observation from a nearby station:")
print(current)
print("\nSun/weather forecast for the selected location/region:")
print(forecast)

# Print the forecasts in a nice format:
print("\nSelected Sun/weather forecast variables in full:")
print("%10s  %16s  %4s  %3s   %3s  %3s  %3s  %3s" % ('UNIX time', 'Date/time CET', 'Rad', 'Sun', 'Cld', 'LCl', 'MCl', 'HCl'))
for row in forecast.iterrows():  # Makes (index, Series) pairs out of row
    # idx = row[0]  # Index
    ser = row[1]  # Data series
    
    # if(float(ser.elev) > 0 and int(ser.sd)==0):
    print("%10i  %16s  %4i  %3i   %3i  %3i  %3i  %3i" %(int(ser.time), ser.cet, int(ser.gr), int(ser.sd), int(ser.tc), int(ser.lc), int(ser.mc), int(ser.hc)))
```

## Meteoserver pages ##

* [Pypi](https://pypi.org/project/meteoserver/): Meteoserver Python package
* [GitHub](https://github.com/MarcvdSluys/Meteoserver): Meteoserver source code


## Author and licence ##

* Author: Marc van der Sluys
* Contact: http://han.vandersluys.nl/en/
* Licence: [GPLv3+](https://www.gnu.org/licenses/gpl.html)


## References ##

* Data, API key and API documentation can be obtained from [Meteoserver.nl](https://meteoserver.nl/)
