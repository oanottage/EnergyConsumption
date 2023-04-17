import pandas as pd
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns

from sklearn.preprocessing import StandardScaler
import pickle

from datetime import datetime
from flask import Flask, render_template, request

import os
os.chdir("/Users/oanottage/Desktop/BTS/BDI/Final_Project/")


# load the model from disk
filename = 'random_forest_model.sav'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

# Load data
df = pd.read_csv('Data_Lake/Silver_Layer/Combined_Data.csv', parse_dates=['date'])

# Convert the date column to a datetime object
df['date'] = pd.to_datetime(df['date'])

# Convert datetime to matplotlib number
df['date_num'] = df['date'].apply(mdates.date2num)

#Removed outliers
df = df[(df['value_energy']<=100000) & (df['value_energy']>=-50000)]




# Home page
@app.route('/')
def index():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Initialization page
@app.route('/init')
def init():

    ########PAGE 1########
    # Create a line plot with seaborn
    sns.lineplot(x='date', y='value_energy', data=df)

    # Add a trend line
    sns.regplot(x='date_num', y='value_energy', data=df)

    # Set the axis labels and title
    plt.xlabel('Date')
    plt.ylabel('Energy Demand Forecast')
    plt.title('Energy Demand Forecasts Over Time')

    # Save the plot to the static folder
    plt.savefig('FlaskApp/static/energy_demand_forecasts.png')

    # Clear the plot to free memory
    plt.clf()

    
    ########PAGE 2########
    # create the scatterplot
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.scatter(df['station'], df['value_weather'], c=df['value_energy'], cmap='coolwarm')
    plt.xlabel('Station')
    plt.ylabel('Value Weather')
    plt.title('Energy Demand Forecasts by Region and Weather Condition')
    
    # Save the plot
    plt.savefig('FlaskApp/static/energy_demand_forecasts_region_weather.png')

    # Clear the plot to free memory
    plt.clf()


    ########PAGE 3########
    # Create a histogram
    plt.hist(df['value_energy'], bins=100)

    # Add x and y-axis labels
    plt.xlabel('Energy Demand Forecast (Megawatt Hours)')
    plt.ylabel('Frequency')

    # Add a title
    plt.title('Distribution of Energy Demand Forecasts')

    # Add a reference line for any outliers or unusual patterns
    plt.axvline(x=5000, color='red', linestyle='dashed')

    # Save the plot
    plt.savefig('FlaskApp/static/distribution_of_energy_demands.png')

    # Clear the plot to free memory
    plt.clf()

    # Render the HTML template
    return render_template('initialize.html')


    


# Page 1: Line plot showing how energy demand forecasts have changed over time
@app.route('/page1')
def page1():    
    # Render the HTML template
    return render_template('page1.html')


# Page 2: Heat map or scatterplot showing how energy demand forecasts vary by region and/or by weather conditions
@app.route('/page2')
def page2():
    # Render the HTML template
    return render_template('page2.html')


# Page 3: Histogram or frequency chart showing the distribution of energy demand forecasts
@app.route('/page3')
def page3():
    # Render the HTML template
    return render_template('page3.html')


# Prediction page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Retrieve the input data
        type_name = request.form['type_name']
        timezone = request.form['timezone']
        station = request.form['station']
        attributes = request.form['attributes']
        value_weather = request.form['value_weather']
        

        # Create a dataframe with the input data
        input_data = pd.DataFrame({
            'type-name_Day-ahead demand forecast': [0],
            'type-name_Demand': [0],
            'type-name_Net generation': [0],
            'type-name_Total interchange': [0],
            'timezone_Arizona': [0],
            'timezone_Central': [0],
            'timezone_Eastern': [0],
            'timezone_Mountain': [0],
            'timezone_Pacific': [0],
            'station_GHCND:USC00280907': [0],
            'station_GHCND:USC00281335': [0],
            'station_GHCND:USC00283704': [0],
            'station_GHCND:USC00284987': [0],
            'station_GHCND:USC00301309': [0],
            'station_GHCND:USC00308577': [0],
            'station_GHCND:USC00309580': [0],
            'station_GHCND:USW00014732': [0],
            'station_GHCND:USW00014734': [0],
            'station_GHCND:USW00054743': [0],
            'station_GHCND:USW00054787': [0],
            'station_GHCND:USW00094728': [0],
            'station_GHCND:USW00094741': [0],
            'station_GHCND:USW00094745': [0],
            'station_GHCND:USW00094789': [0],
            'attributes_,,7,': [0],
            'attributes_,,7,0630': [0],
            'attributes_,,7,0700': [0],
            'attributes_,,7,0800': [0],
            'attributes_,,W,': [0],
            'attributes_,,W,2400': [0],
            'value_weather': [value_weather]
        }) 

        # Update the appropriate columns to 1
        input_data['type-name_' + type_name] = 1
        input_data['timezone_' + timezone] = 1
        input_data['station_' + station] = 1
        input_data['attributes_' + attributes] = 1

        #Apply standard scaler (for the weather value)
        ss = StandardScaler()
        X_scaled = ss.fit_transform(X=input_data)

        # Perform the prediction using the input data
        prediction = model.predict(X_scaled)
        
        # Return the prediction
        return render_template('predict.html', prediction=prediction / 10)
    else:
        # Render the initial page
        return render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True)
