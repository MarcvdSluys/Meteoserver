# -*- coding: utf-8 -*-
#  Copyright (c) 2020-2021  Marc van der Sluys - marc.vandersluys.nl
#  
#  This file is part of the Meteoserver Python package, containing a Python module to obtain and read Dutch
#  weather data from Meteoserver.nl.  See: https://github.com/MarcvdSluys/Meteoserver
#  
#  This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#  
#  This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License along with this code.  If not, see
#  <http://www.gnu.org/licenses/>.


"""
    Functions to print some basic documentation.
"""


def print_help_weatherforecast():
    """Print a brief description for each of the columns for the dataframes containing weather-forecast data."""
    
    print('')
    print('* Columns in forecast dataframe ("data")')
    print('')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| Field      | Description                                                                      |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| tijd       | UNIX timestamp of the current hour (CET(?) in forecast)                          |')
    print('| tijd_nl    | locale date and time in the Nederlands                                           |')
    print('| offset     | hours passed since the weather model was run                                     |')
    print('| loc        | obsolesent; do not use                                                           |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| temp       | current temperature in degrees Celsius                                           |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| winds      | mean wind velocity in m/s                                                        |')
    print('| windb      | mean wind force in Beaufort                                                      |')
    print('| windknp    | mean wind velocity in knots                                                      |')
    print('| windkmh    | mean wind velocity in km/h                                                       |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| windr      | wind direction in degrees                                                        |')
    print('| windrltr   | wind direction abbreviation                                                      |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| gust       | wind gust in m/s (GFS only)                                                      |')
    print('| gustb      | wind gust in Beaufort (GFS only)                                                 |')
    print('| gustkt     | wind gust in knopen (GFS only)                                                   |')
    print('| gustkmh    | wind gust in km/h (GFS only)                                                     |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| vis        | visibility in meters. Available in HARMONIE (Benelux), 50000 means > 50 km. In   |')
    print('|            | GFS up to 121 hours (5 days). After that, the API returns 0 since GFS does not   |')
    print('|            | compute long-term values.  GFS has a different maximum: 25000 means > 25 km.     |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| neersl     | precipitation in mm                                                              |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| luchtd     | air pressure in mbar / hPa                                                       |')
    print('| luchtdmmhg | air pressure in mm Hg                                                            |')
    print('| luchtdinhg | air pressure in inch Hg                                                          |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| rv         | relative humidity in %                                                           |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| gr         | global horizontal radiation: surface downward long-wave radiation flux in W/m²   |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| hw         | percentage of high cloud cover                                                   |')
    print('| mw         | percentage of medium cloud cover                                                 |')
    print('| lw         | percentage of low cloud cover                                                    |')
    print('| tw         | percentage of all cloud cover                                                    |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| cape       | convective available potential energy J/kg, only available in GFS                |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('| cond       | weather condition code                                                           |')
    print('| ico        | weather icon code                                                                |')
    print('| samenv     | short description of weather condition                                           |')
    print('| icoon      | weather image name                                                               |')
    print('|------------+----------------------------------------------------------------------------------|')
    print('')
    
    
def print_help_sunData():
    """Print a brief description for each of the columns for the dataframes containing solar data."""
    
    print('')
    print('* Columns in current measurements dataframe ("current")')
    print('')
    print('Valid for the last 10 minutes')
    print('|---------+------------------------------------------------------------|')
    print('| station | name of KNMI weather station                               |')
    print('| time    | unix timestamp                                             |')
    print('| elev    | current elevation/altitude angle of the Sun (°)            |')
    print('| az      | current azimuth of the Sun (°; N=0, E=90)                  |')
    print('| cet     | local time in the Netherlands (CET/CEST)                   |')
    print('| temp    | temperature (°C)                                           |')
    print('| gr      | global horizontal radiation intensity (J/hr/cm²)           |')
    print('|         |     (WAS IN W/m² until 2021-06-16!!!)                      |')
    print('| gr_w    | global horizontal radiation intensity (W/m²)               |')
    print('|         |     NEW since 2021-06-17!!!                                |')
    print('| sd      | number of sunshine minutes in the current hour             |')
    print('| tc      | total cloud cover (%)                                      |')
    print('| vis     | visibility (meters)                                        |')
    print('| prec    | total precipitation in the current hour (mm(/h))           |')
    print('| sr      | time of sunrise today                                      |')
    print('| ss      | time of sunset today                                       |')
    print('|---------+------------------------------------------------------------|')
    print('')
    print('')
    print('* Columns in hourly forecast dataframe ("forecast")')
    print('')
    print('Valid for the whole hour indicated')
    print('|------+---------------------------------------------------------------|')
    print('| time | unix timestamp                                                |')
    print('| cet  | local time in the Netherlands (CET/CEST)                      |')
    print('| elev | Sun altitude for the start of the current hour (°)            |')
    print('| az   | Sun azimuth for the start of the current hour (°; N=0, E=90)  |')
    print('| temp | temperature (°C)                                              |')
    print('| gr   | global horizontal radiation intensity (J/hr/cm²)              |')
    print('|      |     (WAS IN W/m² until 2021-06-16!!!)                         |')
    print('| gr_w | global horizontal radiation intensity (W/m²)                  |')
    print('|      |     NEW since 2021-06-17!!!                                   |')
    print('| sd   | number of sunshine minutes in the current hour                |')
    print('| tc   | total cloud cover (%)                                         |')
    print('| lc   | low-cloud cover (%)                                           |')
    print('| mc   | intermediate-cloud cover (%)                                  |')
    print('| hc   | high-cloud cover (%)                                          |')
    print('| vis  | visibility (meters; 25000 indicates >= 25km)                  |')
    print('| prec | total precipitation in the current hour (mm(/h))              |')
    print('|------+---------------------------------------------------------------|')
    print('')

    
