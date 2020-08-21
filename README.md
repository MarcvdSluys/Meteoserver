# Meteoserver #

A Python module to obtain and read Dutch weather data from Meteoserver.nl.  The code is being developped by
[Marc van der Sluys](http://han.vandersluys.nl/en/) of the department of Sustainable energy of the HAN
University of Applied Sciences in Arnhem, the Netherlands.


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
meteo.print_help_uurverwachting()

location = 'Unknown'  # Ensure we always have a location 'name' to write to file.

# Read weather-forecast data from file:
# data = meteo.read_json_file_uurverwachting('UurVerwachting1.json', full=True)  # Option 1: HARMONIE/HiRLAM (48 (42?) hours)
# data = meteo.read_json_file_uurverwachting('UurVerwachting2.json')  # Option 2: GFS (4/10 days), useful columns only, no location
# data, location = meteo.read_json_file_uurverwachting('UurVerwachting2.json', full=True, loc=True)  # Option 2, with ALL columns and location

# Get weather-forecast data from server:
# data = meteo.read_json_url_uurverwachting(myKey, myLocation, model='HARMONIE')  # Option 1: HARMONIE/HiRLAM
# data = meteo.read_json_url_uurverwachting(myKey, myLocation)  # Option 2 (default): GFS, useful columns only, no location
data, location = meteo.read_json_url_uurverwachting(myKey, myLocation, full=True, loc=True)  # Option 2, with ALL columns and location

# Print the data:
print(data)

# Write the downloaded data to a json file:
meteo.write_json_file_uurverwachting('UurVerwachting3.json', location, data)



# Sun forecast #####################################################################################

# Print some help:
meteo.print_help_zonactueel()

# Read a Meteoserver Sun-data JSON file from disc:
# current, forecast = meteo.read_json_file_zon('ZonActueel.json')
# current, forecast, location = meteo.read_json_file_zon('ZonActueel.json', loc=True)  # Return the location

# Get Meteoserver Sun data from the server for the given location (and key):
# current, forecast = meteo.read_json_url_zon(myKey, myLocation)
current, forecast, location = meteo.read_json_url_zon(myKey, myLocation, loc=True)  # Return the location

# Print the current-weather and forecast dataframes:
print("\nCurrent Sun/weather observation from a nearby station:")
print(current)

print("\nSun/weather forecast for the selected location/region:")
print(forecast)

# Write the downloaded data to a json file:
meteo.write_json_file_zon('ZonActueel1.json', location, current, forecast)
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
