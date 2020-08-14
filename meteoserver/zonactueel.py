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


"""Functions to obtain and read solar data from Meteoserver.nl.
"""


import pandas as pd
import json
import requests


def read_json_url_zon(key, location):
    """Get the Sun data from the Meteoserver server and return the current-data and forecast dataframes.
    
    Parameters:
        key (string):       The Meteoserver API key.
        location (string):  The name of the location (in the Netherlands) to obtain data for (e.g. 'De Bilt').
    
    Returns:
        tuple (df, df):  Tuple containing (current, forecast):
    
          - current (df):   Pandas dataframe containing current-weather data from a nearby station.
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
    """
    
    # Get online data and return a string containing the json file:
    dataJSON = requests.get('https://data.meteoserver.nl/api/solar.php?locatie='+location+'&key='+key).text
    
    # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam', 'current' and 'forecast':
    dataDict = json.loads(dataJSON)  # Note: .loads(), not .load()!
    
    # Get the current-data and forecast dataframes from the data dictionary:
    current, forecast = extract_Sun_dataframes_from_dict(dataDict)
    
    return current, forecast


def read_json_file_zon(fileJSON):
    """Read a Meteoserver Sun-data JSON file from disc and return the current-data and forecast dataframes.
    
    Parameters:
        fileJSNO (string):  The name of the JSON file to read.
    
    Returns:
        tuple (df, df):  Tuple containing (current, forecast):
    
          - current (df):   Pandas dataframe containing current-weather data from a nearby station.
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
    """
    
    with open(fileJSON) as dataJSON:
        # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam', 'current' and 'forecast':
        dataDict = json.load(dataJSON)  # Note: .load(), not .loads()!
        
        # Get the current-data and forecast dataframes from the data dictionary:
        current, forecast = extract_Sun_dataframes_from_dict(dataDict)
        
    return current, forecast


def extract_Sun_dataframes_from_dict(dataDict):
    """Extract the current-data and forecast Pandas dataframes from a data dictionary.
    
    Parameters:
        dataDict (dict):  The name of the data dictionary to convert.
    
    Returns:
        tuple (df, df):  Tuple containing (current, forecast):
    
          - current (df):   Pandas dataframe containing current-weather data from a nearby station.
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
    """
    
    # print(dataDict.keys())  # Dictionary with keys: ['plaatsnaam', 'current', 'forecast']
    # print(type(dataDict['plaatsnaam']))  # List
    # print(type(dataDict['current']))     # List
    # print(len(dataDict['forecast']))     # List with (112) forecasts
    # for item in dataDict['forecast']:    # Dictionary with forecast data
    #     print("%i  %s  %4i  %2i  %3i" %(int(item['time']), item['cet'], int(item['gr']), int(item['sd']), int(item['tc'])))
        
    # Create Pandas dataframes from lists of dictionaries:
    current = pd.DataFrame.from_dict(dataDict['current'])
    forecast = pd.DataFrame.from_dict(dataDict['forecast'])
    
    # print(current)
    # print(forecast)
    
    return current, forecast


