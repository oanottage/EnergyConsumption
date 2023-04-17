#The usual culprits for data exploration
import pandas as pd

#Prep and Hyperparameter Tuning
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#Model
from sklearn.ensemble import RandomForestRegressor

#Picling the model
import pickle

#Directory change
import os
os.chdir("/Users/oanottage/Desktop/BTS/BDI/Final_Project/")


df = pd.read_csv("Data_Lake/Silver_Layer/Combined_Data.csv", parse_dates=['date'])

# Remove value and datatype (only one value), not necessary
df_combined = df.drop(columns=['value-units','datatype', 'type','timezone-description', 'date', 'respondent','respondent-name'])


#Removed outliers
df_no_outliers = df_combined[(df_combined['value_energy']<=100000) & (df_combined['value_energy']>=-50000)]


#One Hot Encode categorical columns
df_prep = pd.get_dummies(df_combined, columns=['type-name', 'timezone', 'station','attributes'], drop_first=False, dtype=int)


#Split data into training and testing
X = df_prep.drop('value_energy', axis=1)
y = df_prep['value_energy']

#Apply standard scaler (for the weather value)
ss = StandardScaler()
X_scaled = ss.fit_transform(X=X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# create an instance of RandomForestRegressor and fit it to the data
regressor = RandomForestRegressor(n_estimators=100)
regressor.fit(X_train, y_train)

# save the model to disk
filename = 'random_forest_model.sav'
pickle.dump(regressor, open(filename, 'wb'))