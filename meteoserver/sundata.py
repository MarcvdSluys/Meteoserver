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


"""Functions to obtain, read and write four-day sun-forecast ("Zon Actueel") data from Meteoserver.nl.

"""


import pandas as pd
import json
import requests


def read_json_url_sunData(key, location, loc=False):
    """Get the Sun data from the Meteoserver server and return the current-data and forecast dataframes and
       optionally the location name.
    
    This uses the "Zon Actueel" Meteoserver API/data.
    
    Parameters:
        key (string):       The Meteoserver API key.
        location (string):  The name of the location (in the Netherlands) to obtain data for (e.g. 'De Bilt').
        loc (bool):         Return the location name as a third return value (default=False).
    
    Returns:
        tuple (df, df (,str)):  Tuple containing (current, forecast (, location)):
    
          - current (df):   Pandas dataframe containing current-weather data from a nearby station.
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
          - retLoc (str):   The name of the location the data are for (only returned if loc=True).
    """
    
    # Get online data and return a string containing the json file:
    dataJSON = requests.get('https://data.meteoserver.nl/api/solar.php?locatie='+location+'&key='+key).text
    
    # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam', 'current' and 'forecast':
    dataDict = json.loads(dataJSON)  # Note: .loads(), not .load()!
    
    # Get the current-data and forecast dataframes from the data dictionary:
    retLoc, current, forecast = extract_Sun_dataframes_from_dict(dataDict)
    
    if(loc):
        return current, forecast, retLoc
    else:
        return current, forecast


def read_json_file_sunData(fileJSON, loc=False):
    """Read a Meteoserver Sun-data JSON file from disc and return the current-data and forecast dataframes, and
       optionally the location name.
    
    This uses the "Zon Actueel" Meteoserver data.
    
    Parameters:
        fileJSNO (string):  The name of the JSON file to read.
        loc (bool):         Return the location name as a third return value (default=False).
    
    Returns:
        tuple (df, df (,str)):  Tuple containing (current, forecast (, location)):
    
          - current (df):   Pandas dataframe containing current-weather data from a nearby station.
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
          - location (str): The location the data are for.

    """
    
    with open(fileJSON) as dataJSON:
        # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam', 'current' and 'forecast':
        dataDict = json.load(dataJSON)  # Note: .load(), not .loads()!
        
        # Get the location, current-data and forecast dataframes from the data dictionary:
        location, current, forecast = extract_Sun_dataframes_from_dict(dataDict)
        
    if(loc):
        return current, forecast, location
    else:
        return current, forecast


def extract_Sun_dataframes_from_dict(dataDict):
    """Extract the location name, current-data and forecast Pandas dataframes from a data dictionary.
    
    Parameters:
        dataDict (dict):  The name of the data dictionary to convert.
    
    Returns:
        tuple (str, df, df):  Tuple containing (location, current, forecast):
    
          - current (df):   Pandas dataframe containing current-weather data from a nearby station.
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
          - forecast (df):  Pandas dataframe containing forecast data for the specified location (or region?).
    """
    
    # print(dataDict.keys())  # Dictionary with keys: ['plaatsnaam', 'current', 'forecast']
    # print(type(dataDict['plaatsnaam']))  # List
    # print(type(dataDict['current']))     # List
    # print(len(dataDict['forecast']))     # List with (112) forecasts
    # for item in dataDict['forecast']:    # Dictionary with forecast data
    #     print("%i  %s  %4i  %2i  %3i" %(int(item['time']), item['cet'], int(item['gr']), int(item['sd']), int(item['tc'])))
        
    # Create Pandas dataframes from lists of dictionaries:
    location = pd.DataFrame.from_dict(dataDict['plaatsnaam']).plaats[0]  # List of dict -> df -> str
    current = pd.DataFrame.from_dict(dataDict['current'])
    forecast = pd.DataFrame.from_dict(dataDict['forecast'])
    
    # print(current)
    # print(forecast)
    
    return location, current, forecast


def write_json_file_sunData(fileName, location, current, forecast):
    """Write a Meteoserver sun-forecast-data JSON file to disc.
    
    The resulting file has the same format as a downloaded file (barring some spacing).
    
    Parameters:
        fileName (string):  The name of the JSON file to write.
        location (string):  The location the data are for.
        current (df):       Pandas dataframe containing current/recent measurements for the specified location (or region).
        forecast (df):      Pandas dataframe containing sun forecast data for the specified location (or region).
    """
    
    # Convert location string into a dict:
    locationDict = {}
    locationDict['plaats'] = location
    
    # Convert current dataframe into a dict:
    currentDict = current.to_dict(orient='records')
    
    # Convert forecast dataframe into a dict:
    forecastDict = forecast.to_dict(orient='records')
    
    # Put the dicts into an enveloping dict:
    fileJSON = {}
    
    # Add the location:
    fileJSON['plaatsnaam'] = []
    fileJSON['plaatsnaam'].append(locationDict)
    
    # Add the current measurements:
    fileJSON['current'] = currentDict
    
    # Add the forecast data:
    fileJSON['forecast'] = forecastDict
    
    # Write the resulting dictionary to a json file:
    with open(fileName, 'w') as outFile:
        json.dump(fileJSON, outFile)
    
    return


