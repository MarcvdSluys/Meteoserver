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


def read_json_url_sunData(key, location, loc=False, numeric=True):
    """Get the Sun data from the Meteoserver server and return the current-data and forecast dataframes and
    optionally the location name.
    
    This uses the "Zon Actueel" Meteoserver API/data.
    
    Parameters:
        key (string):       The Meteoserver API key.
        location (string):  The name of the location (in the Netherlands) to obtain data for (e.g. 'De Bilt').
        loc (bool):         Return the location name as a third return value (default=False).
        numeric (bool):     Convert dataframe content from strings to numeric/datetime format (default=True).
                            Set this to False if you intend to write a JSON file that is (nearly) identical
                            to the original format.
    
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
    retLoc, current, forecast = extract_Sun_dataframes_from_dict(dataDict, numeric)
    
    if(loc):
        return current, forecast, retLoc
    else:
        return current, forecast


def read_json_file_sunData(fileJSON, loc=False, numeric=True):
    """Read a Meteoserver Sun-data JSON file from disc and return the current-data and forecast dataframes, and
    optionally the location name.
    
    This uses the "Zon Actueel" Meteoserver data.
    
    Parameters:
        fileJSNO (string):  The name of the JSON file to read.
        loc (bool):         Return the location name as a third return value (default=False).
        numeric (bool):     Convert dataframe content from strings to numeric/datetime format (default=True).
                            Set this to False if you intend to write a JSON file that is (nearly) identical
                            to the original format.
    
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
        location, current, forecast = extract_Sun_dataframes_from_dict(dataDict, numeric)
        
    if(loc):
        return current, forecast, location
    else:
        return current, forecast


def extract_Sun_dataframes_from_dict(dataDict, numeric):
    """Extract the location name, current-data and forecast Pandas dataframes from a data dictionary.
    
    Parameters:
        dataDict (dict):  The name of the data dictionary to convert.
        numeric (bool):   Convert dataframe content from strings to numeric/datetime format (default=True).
                          Set this to False if you intend to write a JSON file that is (nearly) identical
                          to the original format.
    
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
        
    # Convert the 'plaatsnaam' list of dictionaries to a string containing the location name:
    location = pd.DataFrame.from_dict(dataDict['plaatsnaam']).plaats[0]  # List of dict -> df -> str
    
    
    # Convert the 'current' list of dictionaries to Pandas dataframe:
    current = pd.DataFrame.from_dict(dataDict['current'])
    
    # Convert the df elements to numeric/datetime types:
    if(numeric):
        # Add date from 'cet' column to sunrise and sunset (while 'cet' is still a string):
        if('sr' in current.columns):
            current.sr = current.cet.str.slice(0,10) + ' ' + current.sr  # Create a string from the first 10 characters of the date + space + time
            current.sr = pd.to_datetime(current.sr, format='%d-%m-%Y %H:%M',  errors='coerce')  # String -> datetime
        
        if('ss' in current.columns):
            current.ss = current.cet.str.slice(0,10) + ' ' + current.ss  # Create a string from the first 10 characters of the date + space + time
            current.ss = pd.to_datetime(current.ss, format='%d-%m-%Y %H:%M',  errors='coerce')  # String -> datetime
        
        
        if('time' in current.columns):  current.time = pd.to_numeric(current.time,  errors='coerce').values
        if('cet'  in current.columns):  current.cet  = pd.to_datetime(current.cet, format='%d-%m-%Y %H:%M',  errors='coerce')
        if('elev' in current.columns):  current.elev = pd.to_numeric(current.elev,  errors='coerce').values
        if('az'   in current.columns):  current.az   = pd.to_numeric(current.az,    errors='coerce').values
        if('temp' in current.columns):  current.temp = pd.to_numeric(current.temp,  errors='coerce').values
        if('gr'   in current.columns):  current.gr   = pd.to_numeric(current.gr,    errors='coerce').values
        if('sd'   in current.columns):  current.sd   = pd.to_numeric(current.sd,    errors='coerce').values
        if('tc'   in current.columns):  current.tc   = pd.to_numeric(current.tc,    errors='coerce').values
        if('vis'  in current.columns):  current.vis  = pd.to_numeric(current.vis,   errors='coerce').values
        if('prec' in current.columns):  current.prec = pd.to_numeric(current.prec,  errors='coerce').values
    
    # print(current)
    
    
    # Convert the 'forecast' list of dictionaries to Pandas dataframe:
    forecast = pd.DataFrame.from_dict(dataDict['forecast'])
    
    # Convert the df elements to numeric/datetime types:
    if(numeric):
        if('time' in forecast.columns):  forecast.time = pd.to_numeric(forecast.time,  errors='coerce').values
        if('cet'  in forecast.columns):  forecast.cet  = pd.to_datetime(forecast.cet, format='%d-%m-%Y %H:%M',  errors='coerce')
        if('elev' in forecast.columns):  forecast.elev = pd.to_numeric(forecast.elev,  errors='coerce').values
        if('az'   in forecast.columns):  forecast.az   = pd.to_numeric(forecast.az,    errors='coerce').values
        if('temp' in forecast.columns):  forecast.temp = pd.to_numeric(forecast.temp,  errors='coerce').values
        if('gr'   in forecast.columns):  forecast.gr   = pd.to_numeric(forecast.gr,    errors='coerce').values
        if('sd'   in forecast.columns):  forecast.sd   = pd.to_numeric(forecast.sd,    errors='coerce').values
        if('tc'   in forecast.columns):  forecast.tc   = pd.to_numeric(forecast.tc,    errors='coerce').values
        if('lc'   in forecast.columns):  forecast.lc   = pd.to_numeric(forecast.lc,    errors='coerce').values
        if('mc'   in forecast.columns):  forecast.mc   = pd.to_numeric(forecast.mc,    errors='coerce').values
        if('hc'   in forecast.columns):  forecast.hc   = pd.to_numeric(forecast.hc,    errors='coerce').values
        if('vis'  in forecast.columns):  forecast.vis  = pd.to_numeric(forecast.vis,   errors='coerce').values
        if('prec' in forecast.columns):  forecast.prec = pd.to_numeric(forecast.prec,  errors='coerce').values
    
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
    fileJSON = json.dumps(fileJSON, indent=None, separators=(',',':'), default=str)  # Create a JSON string, even with non-serialisable Timestamps - https://stackoverflow.com/a/36142844/1386750.  This adds " and ecapes existing ones.
    outFile = open(fileName,'w')
    outFile.write(fileJSON+'\n')  # Needs '\n' to match server version.
    outFile.close()
    return

    # with open(fileName, 'w') as outFile:
    #     try:
    #         json.dump(fileJSON, outFile)
    #     except Exception as e:
    #         print("An error occurred when creating the JSON output file "+fileName+": ", end='')
    #         print(e)
    #         print("Did you forget to specify 'numeric=False' when reading the solar data?")
    #         print("Aborting.")
    #         exit(1)
    #         
    # return
    

