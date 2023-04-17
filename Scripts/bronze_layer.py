import pandas as pd
import json
import requests
import os
from datetime import datetime, timedelta
os.chdir("/Users/oanottage/Desktop/BTS/BDI/Final_Project/")

today = datetime.today().date()
week_ago = today - timedelta(days=7)

#Energy API Data Collection
def energy_bronze():
    url = "https://api.eia.gov/v2/electricity/rto/daily-region-data/data/"
    params = {
        "api_key":"pfHsG8Kz0n6lk2qkEvOUdEfip5uJeCeeBGQqfMqa",
        "frequency": "daily",
        "data[0]": "value",
        "start": week_ago,
        "end": week_ago,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": "0",
        "length": "10000"
    }

    response = requests.get(url, params=params)

    # Convert response content to dictionary
    data = json.loads(response.content.decode('utf-8'))

    # Extract the data as a list of dictionaries
    data_list = data['response']['data']

    # Create pandas dataframe from the list of dictionaries
    energy_df = pd.DataFrame(data_list)
    energy_df.to_csv(f"Data_Lake/Bronze_Layer/Energy_Daily_Region_{week_ago}.csv",index=False)
    return


#Weather API Data Collection
def weather_bronze():
  url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&locationid=CITY:US360019&startdate={week_ago}&enddate={week_ago}&limit=1000"
  token = "vEExMEAzWdmnwblNYcNKBaIaasvEqEAm"

  # Using requests to send a GET request with token header
  headers = {"token": token}
  response = requests.get(url, headers=headers)

  # Load the JSON response into a dictionary
  data = json.loads(response.content.decode('utf-8'))

  # Extract the data as a list of dictionaries
  data_list = data['results']

  # Create pandas dataframe from the list of dictionaries
  weather_df = pd.DataFrame(data_list)
  weather_df.to_csv(f"Data_Lake/Bronze_Layer/Daily_Weather_{week_ago}.csv",index=False)
  return


#Putting it All Together
def bronze():
  energy_bronze()
  weather_bronze()
  return

bronze()