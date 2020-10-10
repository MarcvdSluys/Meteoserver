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


"""Functions to obtain, read and write 2 (HARMONIE) or 4-10 (GFS) day hourly weather-forecast
   ("Uurverwachting") data from Meteoserver.nl.
"""


import pandas as pd
import json
import requests
import sys



def read_json_url_weatherforecast(key, location, model='GFS', full=False, loc=False, numeric=True):
    """Get hourly weather-forecast data from the Meteoserver server and return them as a dataframe.
    
    This uses the "Uurverwachting" Meteoserver API/data.
    
    Parameters:
        key (string):       The Meteoserver API key.
        location (string):  The name of the location (in the Netherlands) to obtain data for (e.g. 'De Bilt').
        model (string):     Weather model to use: 'HARMONIE' or 'GFS' (default: GFS)
    
                                - HARMONIE: use high-resolution HARMONIE model for BeNeLux and HiRLAM for the
                                  rest of Europe.  Hourly predictions up to 48 hours in advance.  New data
                                  available at 5:30, 11:30, 17:30 and 23:30 CE(S)T.
    
                                - GFS: use GFS model for BeNeLux.  Hourly predictions for 4 days, then
                                  three-hourly predictions for the next 10 days.  New data are available at
                                  0:30, 7:30, 12:30 and 18:30 CE(S)T.
    
        full (bool):        Return the full dataframe (currently 31 columns).  If false, obsolescent and duplicate 
                            (in non-SI units) columns are removed (currently, 22 columns are returned).  Default: False.
        loc (bool):         Return the location name as a second return value (default=False).
        numeric (bool):     Convert dataframe content from strings to numeric/datetime format (default=True).
                            Set this to False if you intend to write a JSON file that is (nearly) identical
                            to the original format.
    
    Returns:
        tuple (df, str):  Tuple containing (data, retLoc):
    
          - data (df):     Pandas dataframe containing forecast data for the specified location (or region).
          - retLoc (str):  The name of the location the data are for (only returned if loc=True - in this case,
            the two return values are returned as a tuple).

    """
    
    # Get online data and return a string containing the json file:
    if(model == 'GFS'):
        dataJSON = requests.get('https://data.meteoserver.nl/api/uurverwachting_gfs.php?locatie='+location+'&key='+key).text
    elif(model == 'HARMONIE'):
        dataJSON = requests.get('https://data.meteoserver.nl/api/uurverwachting.php?locatie='+location+'&key='+key).text
    else:
        print("read_json_url_weatherforecast(): error: unknown model: "+model+'; please choose between HARMONIE and GFS',
              file=sys.stderr)
        exit(1)
        
    # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam' and 'data':
    dataDict = json.loads(dataJSON)  # Note: .loads(), not .load()!
    
    # Get the location name and forecast-data dataframe from the data dictionary:
    retLoc, data = extract_hourly_forecast_dataframes_from_dict(dataDict, numeric)
    
    if(not full):  # Remove obsolescent and duplicate columns:
        data = remove_unused_hourly_forecast_columns(data)
        
    if(loc):
        return data, retLoc
    else:
        return data


def read_json_file_weatherforecast(fileJSON, full=False, loc=False, numeric=True):
    """Read a Meteoserver weather-forecast-data JSON file from disc and return the data as a dataframe.
    
    This uses the "Uurverwachting" Meteoserver data.
    
    Parameters:
        fileJSNO (string):  The name of the JSON file to read.
        full (bool):        Return the full dataframe (currently 31 columns).  If false, obsolescent and duplicate 
                            (in non-SI units) columns are removed (currently, 22 columns are returned).  Default: False.
        loc (bool):         Return the location name as a second return value (default=False).
        numeric (bool):     Convert dataframe content from strings to numeric/datetime format (default=True).
                            Set this to False if you intend to write a JSON file that is (nearly) identical
                            to the original format.
    
    Returns:
        tuple (df, str):   Tuple containing (data, location):
    
        - data (df):       Pandas dataframe containing forecast data for the specified location (or region).
        - location (str):  The name of the location the data are for (only returned if loc=True) - in this case, 
          the two return values are returned as a tuple).
    
    """
    
    with open(fileJSON) as dataJSON:
        # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam' and 'data':
        dataDict = json.load(dataJSON)  # Note: .load(), not .loads()!
        
        # Get the location name and forecast-data dataframe from the data dictionary:
        location, data = extract_hourly_forecast_dataframes_from_dict(dataDict, numeric)
        
        if(not full):  # Remove obsolescent and duplicate columns:
            data = remove_unused_hourly_forecast_columns(data)

    if(loc):
        return data, location
    else:
        return data


def extract_hourly_forecast_dataframes_from_dict(dataDict, numeric):
    """Extract the location and forecast-data Pandas dataframe from a data dictionary.
    
    Parameters:
        dataDict (dict):  The data dictionary to convert.
        numeric (bool):   Convert dataframe content from strings to numeric/datetime format (default=True).
                          Set this to False if you intend to write a JSON file that is (nearly) identical
                          to the original format.
    
    Returns:
        tuple (str, df):  Tuple containing (location, data):
        
          - location (str):  Location the data are for.
          - data (df):       Pandas dataframe containing forecast data for the specified location (or region).
    """
    
    # print(dataDict.keys())  # Dictionary with keys: ['plaatsnaam' and 'data']
    # print(type(dataDict['plaatsnaam']))  # List of 1 dict containing a location name
    # print(type(dataDict['data']), len(dataDict['data']))       # List with (152) forecasts
    
    # Create location string from list of dictionaries:
    location = pd.DataFrame.from_dict(dataDict['plaatsnaam']).plaats[0]  # List of dict -> df -> str
    
    # Create Pandas dataframe from list of dictionaries:
    data = pd.DataFrame.from_dict(dataDict['data'])
    
    # Convert df elements to numeric values:
    if(numeric):
        if('tijd'       in data.columns):  data['tijd']       = pd.to_numeric(data['tijd'],        errors='coerce')
        if('tijd_nl'    in data.columns):  data['tijd_nl']    = pd.to_datetime(data['tijd_nl'], format='%d-%m-%Y %H:%M', errors='coerce')
        if('offset'     in data.columns):  data['offset']     = pd.to_numeric(data['offset'],      errors='coerce')
        if('loc'        in data.columns):  data['loc']        = pd.to_numeric(data['loc'],         errors='coerce')
        if('temp'       in data.columns):  data['temp']       = pd.to_numeric(data['temp'],        errors='coerce')
        if('winds'      in data.columns):  data['winds']      = pd.to_numeric(data['winds'],       errors='coerce')
        if('windb'      in data.columns):  data['windb']      = pd.to_numeric(data['windb'],       errors='coerce')
        if('windknp'    in data.columns):  data['windknp']    = pd.to_numeric(data['windknp'],     errors='coerce')
        if('windkmh'    in data.columns):  data['windkmh']    = pd.to_numeric(data['windkmh'],     errors='coerce')
        if('windr'      in data.columns):  data['windr']      = pd.to_numeric(data['windr'],       errors='coerce')
        # data['windrltr']  =  pd.to_numeric(data['windrltr'])
        if('gust'       in data.columns):  data['gust']       = pd.to_numeric(data['gust'],        errors='coerce')
        if('gustb'      in data.columns):  data['gustb']      = pd.to_numeric(data['gustb'],       errors='coerce')
        if('gustkt'     in data.columns):  data['gustkt']     = pd.to_numeric(data['gustkt'],      errors='coerce')
        if('gustkmh'    in data.columns):  data['gustkmh']    = pd.to_numeric(data['gustkmh'],     errors='coerce')
        if('vis'        in data.columns):  data['vis']        = pd.to_numeric(data['vis'],         errors='coerce')
        if('neersl'     in data.columns):  data['neersl']     = pd.to_numeric(data['neersl'],      errors='coerce')
        if('luchtd'     in data.columns):  data['luchtd']     = pd.to_numeric(data['luchtd'],      errors='coerce')
        if('luchtdmmhg' in data.columns):  data['luchtdmmhg'] = pd.to_numeric(data['luchtdmmhg'],  errors='coerce')
        if('luchtdinhg' in data.columns):  data['luchtdinhg'] = pd.to_numeric(data['luchtdinhg'],  errors='coerce')
        if('rv'         in data.columns):  data['rv']         = pd.to_numeric(data['rv'],          errors='coerce')
        if('gr'         in data.columns):  data['gr']         = pd.to_numeric(data['gr'],          errors='coerce')
        if('hw'         in data.columns):  data['hw']         = pd.to_numeric(data['hw'],          errors='coerce')
        if('mw'         in data.columns):  data['mw']         = pd.to_numeric(data['mw'],          errors='coerce')
        if('lw'         in data.columns):  data['lw']         = pd.to_numeric(data['lw'],          errors='coerce')
        if('tw'         in data.columns):  data['tw']         = pd.to_numeric(data['tw'],          errors='coerce')
        if('cape'       in data.columns):  data['cape']       = pd.to_numeric(data['cape'],        errors='coerce')
        if('cond'       in data.columns):  data['cond']       = pd.to_numeric(data['cond'],        errors='coerce')
        if('ico'        in data.columns):  data['ico']        = pd.to_numeric(data['ico'],         errors='coerce')
    
    # print(type(location))
    # print(data)
    
    return location, data


def remove_unused_hourly_forecast_columns(dataFrame):
    """Remove the (probably) unused columns from a weather-forecast dataframe.
    
    This removes the following columns (if they exist):
      - obsolescent 'loc' column.
      - wind speed/force 'windb' (Beaufort), 'windknp' (knots) and 'windkmh' (km/h) columns, which can be computed 
        from SI 'winds' (m/s) column.
      - wind gust columns: 'gustb' (Beaufort), 'gustkt' (knots) and 'gustkmh', which can be computed from SI 'gust' 
        column (m/s).
      - air-pressure columns: 'luchtdmmhg' and 'luchtdinhg', which can be computed from SI luchtd (hPa/mbar).
    
    The number of columns is reduced from 27 to 21 for HARMONIE data, and from 31 to 22 for GFS data.
    
    
    Parameters:
        dataFrame (df):  Original Pandas dataframe.
    
    Returns:
        dataFrame (df):  Pruned Pandas dataframe.
    """
    
    # Obsolescent 'loc' column:
    if('loc' in dataFrame.columns):
        del dataFrame['loc']
        
    # Remove 'windb' (Beaufort), 'windknp' (knots) and 'windkmh' columns, as they can be computed from SI winds (m/s):
    if('windb' in dataFrame.columns):
        del dataFrame['windb']
    if('windknp' in dataFrame.columns):
        del dataFrame['windknp']
    if('windkmh' in dataFrame.columns):
        del dataFrame['windkmh']
    
    # Remove 'gustb' (Beaufort), 'gustkt' (knots) and 'gustkmh' columns, as they can be computed from SI gust (m/s):
    if('gustb' in dataFrame.columns):
        del dataFrame['gustb']
    if('gustkt' in dataFrame.columns):
        del dataFrame['gustkt']
    if('gustkmh' in dataFrame.columns):
        del dataFrame['gustkmh']
    
    # Remove 'luchtdmmhg' and 'luchtdinhg' columns, as they can be computed from (~SI) luchtd (hPa/mbar):
    if('luchtdmmhg' in dataFrame.columns):
        del dataFrame['luchtdmmhg']
    if('luchtdinhg' in dataFrame.columns):
        del dataFrame['luchtdinhg']

    return dataFrame


def write_json_file_weatherforecast(fileName, location, data):
    """Write a Meteoserver weather-forecast-data JSON file to disc.
    
    The resulting file has the same format as a downloaded file (barring some spacing).
    
    Parameters:
        fileName (string):  The name of the JSON file to write.
        location (string):  The location the data are for.
        data (df):          Pandas dataframe containing forecast data for the specified location (or region).
    """
    
    # Convert location string into a dict:
    locationDict = {}
    locationDict['plaats'] = location
    
    # Convert data dataframe into a dict:
    dataDict = data.to_dict(orient='records')
    
    # Put the dicts into an enveloping dict:
    fileJSON = {}
    
    # Add the location:
    fileJSON['plaatsnaam'] = []
    fileJSON['plaatsnaam'].append(locationDict)
    
    # Add the data:
    fileJSON['data'] = dataDict
    
    # Write the resulting dictionary to a json file:
    fileJSON = json.dumps(fileJSON, indent=None, separators=(',',':'), default=str)  # Create a JSON string, even with non-serialisable Timestamps - https://stackoverflow.com/a/36142844/1386750.  This adds " and ecapes existing ones.
    outFile = open(fileName,'w')
    outFile.write(fileJSON)
    outFile.close()
    return

    # with open(fileName, 'w') as outFile:
    #     json.dump(fileJSON, outFile)
    # 
    # return


