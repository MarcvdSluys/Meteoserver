#  Copyright (c) 2020  Marc van der Sluys - marc.vandersluys.nl
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


"""Functions to print some basic documentation.
"""


def print_help_zonactueel():
    print('')
    print('* Current measurements ("current")')
    print('')
    print('Valid for the last 10 minutes')
    print('|---------+------------------------------------------------------------|')
    print('| station | name of KNMI weather station                               |')
    print('| time    | unix timestamp                                             |')
    print('| elev    | current elevation/altitude angle of the Sun (°)            |')
    print('| az      | current azimuth of the Sun (°; N=0, E=90)                  |')
    print('| cet     | local time in the Netherlands (CET/CEST)                   |')
    print('| temp    | temperature (°C)                                           |')
    print('| gr      | global (horizontal?) radiation intensity (W/m²)            |')
    print('| sd      | number of sunshine minutes in the current hour             |')
    print('| tc      | total cloud cover (%)                                      |')
    print('| vis     | visibility (meters)                                        |')
    print('| prec    | total precipitation in the current hour (mm(/h))           |')
    print('| sr      | time of sunrise today                                      |')
    print('| ss      | time of sunset today                                       |')
    print('|---------+------------------------------------------------------------|')
    print('')
    print('')
    print('* Hourly forecast ("forecast")')
    print('')
    print('Valid for the whole hour indicated')
    print('|------+---------------------------------------------------------------|')
    print('| time | unix timestamp                                                |')
    print('| cet  | local time in the Netherlands (CET/CEST)                      |')
    print('| elev | Sun altitude for the start of the current hour (°)            |')
    print('| az   | Sun azimuth for the start of the current hour (°; N=0, E=90)  |')
    print('| temp | temperature (°C)                                              |')
    print('| gr   | global (horizontal?) radiation intensity (W/m²)               |')
    print('| sd   | number of sunshine minutes in the current hour                |')
    print('| tc   | total cloud cover (%)                                         |')
    print('| lc   | low-cloud cover (%)                                           |')
    print('| mc   | intermediate-cloud cover (%)                                  |')
    print('| hc   | high-cloud cover (%)                                          |')
    print('| vis  | visibility (meters; 25000 indicates >= 25km)                  |')
    print('| prec | total precipitation in the current hour (mm(/h))              |')
    print('|------+---------------------------------------------------------------|')
    print('')

    
