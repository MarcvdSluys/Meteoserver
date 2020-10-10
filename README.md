# Meteoserver #

A Python module to obtain and read Dutch weather data from Meteoserver.nl.  The code is being developped by
[Marc van der Sluys](http://han.vandersluys.nl/en/) of the department of Astrophysics at the Radboud
University Nijmegen, the Netherlands and the department of Sustainable energy of the HAN University of Applied
Sciences in Arnhem, the Netherlands.


## Installation ##

This package can be installed using `pip install meteoserver`.  This should automatically install the
dependency packages `pandas` and `requests`, if they haven't been installed already.  If you are installing by
hand, ensure that these packages are installed as well.

You will need to obtain a (free) account and API key at [Meteoserver.nl](https://meteoserver.nl/) to download
data from the Meteoserver API.


## Example use ##

```python
"""Example Python script using the Meteoserver module."""

import meteoserver as meteo

myKey = 'a123456789'    # My Meteoserver API key - put your OWN key here!
myLocation = 'De Bilt'  # My location

# Weather forecast #################################################################################

# Print some help:
meteo.print_help_weatherforecast()

location = 'Unknown'  # Ensure we always have a location 'name' to write to file.

# Read weather-forecast data from file:
# data = meteo.read_json_file_weatherforecast('WeatherForecast1.json', full=True)  # Option 1: HARMONIE/HiRLAM (48 (42?) hours)
# data = meteo.read_json_file_weatherforecast('WeatherForecast2.json')  # Option 2: GFS (4/10 days), useful columns only, no location
# Option 2, with ALL columns and location; don't convert to numerical format, to allow writing to file later:
# data, location = meteo.read_json_file_weatherforecast('WeatherForecast2.json', full=True, loc=True, numeric=False)

# Get weather-forecast data from server:
# data = meteo.read_json_url_weatherforecast(myKey, myLocation, model='HARMONIE')  # Option 1: HARMONIE/HiRLAM
# data = meteo.read_json_url_weatherforecast(myKey, myLocation)  # Option 2 (default): GFS, useful columns only, no location
# Option 2, with ALL columns and location; don't convert to numerical format, to allow writing to file later:
data, location = meteo.read_json_url_weatherforecast(myKey, myLocation, full=True, loc=True, numeric=False)

# Print the data:
print(data)

# Write the downloaded data to a json file:
meteo.write_json_file_weatherforecast('WeatherForecast3.json', location, data)



# Sun forecast #####################################################################################

# Print some help:
meteo.print_help_sunData()

# Read a Meteoserver Sun-data JSON file from disc:
# current, forecast = meteo.read_json_file_sunData('SunData.json')
# Return the location; don't convert to numerical format, to allow writing to file later:
# current, forecast, location = meteo.read_json_file_sunData('SunData.json', loc=True, numeric=False)

# Get Meteoserver Sun data from the server for the given location (and key):
# current, forecast = meteo.read_json_url_sunData(myKey, myLocation)
# Return the location; don't convert to numerical format, to allow writing to file later:
current, forecast, location = meteo.read_json_url_sunData(myKey, myLocation, loc=True, numeric=False)

# Print the current-weather and forecast dataframes:
print("\nCurrent Sun/weather observation from a nearby station:")
print(current)

print("\nSun/weather forecast for the selected location/region:")
print(forecast)

# Write the downloaded data to a json file:
meteo.write_json_file_sunData('SunData1.json', location, current, forecast)
```

## Meteoserver pages ##

* [Pypi](https://pypi.org/project/meteoserver/): Meteoserver Python package
* [GitHub](https://github.com/MarcvdSluys/Meteoserver/): Meteoserver source code
* [ReadTheDocs](https://meteoserver.readthedocs.io/): Meteoserver documentation


## Author and licence ##

* Author: Marc van der Sluys
* Contact: http://han.vandersluys.nl/en/
* Licence: [GPLv3+](https://www.gnu.org/licenses/gpl.html)


## References ##

* Data, API key and API documentation can be obtained from [Meteoserver.nl](https://meteoserver.nl/)
