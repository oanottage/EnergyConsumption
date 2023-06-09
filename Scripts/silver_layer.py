import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta
os.chdir("/Users/oanottage/Desktop/BTS/BDI/Final_Project/")

today = datetime.today().date()
week_ago = today - timedelta(days=7)

#Combined Energy and Weather
def combined_silver():
  weather_df = pd.read_csv(f"Data_Lake/Bronze_Layer/Daily_Weather_{week_ago}.csv", parse_dates=['date'])
  energy_df = pd.read_csv(f"Data_Lake/Bronze_Layer/Energy_Daily_Region_{week_ago}.csv", parse_dates=['period']).rename(columns={'period': 'date'})
  combined_df = energy_df.merge(weather_df, on='date', how='left', suffixes=['_energy','_weather'])
  combined_df['date'] = combined_df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
  combined_df.to_csv(f"Data_Lake/Silver_Layer/Combined_Data_{week_ago}.csv",index=False)
  combined_df.to_parquet(f"Data_Lake/Silver_Layer/Combined_Data_{week_ago}.parquet",index=False)

  #Rename columns for combined database
  combined_df.columns = ['date', 'respondent', 'respondent_name', 'type', 'type_name',
       'timezone', 'timezone_description', 'value_energy', 'value_units',
       'datatype', 'station', 'attributes', 'value_weather']
  
  #Dynamic Insertion into Database
  #Connect to BDI Database and Create Table if not exists
  cnx = sqlite3.connect('Data_Lake/Databases/EnergyWeatherDB.db')
  c = cnx.cursor()
  c.execute("CREATE TABLE IF NOT EXISTS combined(Date TEXT, Respondent TEXT, Respondent_Name TEXT, Type TEXT, Type_Name TEXT, Timezone TEXT, Timezone_Description TEXT, Energy_Value INTEGER, Energy_Units TEXT, Datatype TEXT, Station TEXT, Attributes TEXT, Weather_Value INTEGER)")

  #Insert Energy and Weather fields into database
  for index, row in combined_df.iterrows():
     c.execute("INSERT INTO combined(Date, Respondent, Respondent_Name, Type, Type_Name, Timezone, Timezone_Description, Energy_Value, Energy_Units, Datatype, Station, Attributes, Weather_Value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
     (row.date, row.respondent, row.respondent_name, row.type, row.type_name, row.timezone, row.timezone_description, row.value_energy, row.value_units, row.datatype, row.station, row.attributes, row.value_weather)) 
     cnx.commit()
  c.close()
  cnx.close()
  
  return


def silver():
  combined_silver()
  return 

silver()