# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:44:42 2023

@author: john4
"""

from sklearn import preprocessing
import pandas as pd
import sys


START_YEAR = 1950
END_YEAR = 2023



def normalize_data(data):
    
    normalized_data = preprocessing.normalize([data])
    
    
    #scaler = preprocessing.MinMaxScaler()
    #scaler.fit(data) # Compute the minimum and maximum to be used for later scaling.
    #scaler.transform(data) # Scale features of X according to feature_range.
    
    #return  scaler.transform(data)
    return normalized_data
    



def get_sp500_data():
    SP500_data = (
        pd.read_csv("data/sp500_data.csv")
        .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
        .sort_values(by="Date")
    )
    
    #print(SP500_data.head())
    #print(SP500_data.columns)
    #print(SP500_data.tail())
    
    # Getting rid of the commas in the numbers for casting
    SP500_data['Close*'] = SP500_data['Close*'].str.replace(",", "")
    
    # Cast to float
    SP500_data['Close*'] = SP500_data['Close*'].astype(float)
    
    # Normalize data
    test = normalize_data(SP500_data['Close*'])
    SP500_data['Close*'] = test[0]
    
    SP500_data.drop(columns=['Open', 'High', 'Low', 'Adj Close**', 'Volume'], inplace=True)
    
    #SP500_data.rename(columns={"Close*": "to_plot"})
    
    return SP500_data



def get_interest_rate_data():
    interest_data = (
        pd.read_csv("data/kaggle_fed_interest_rate_1954.csv", usecols = ['Year', 'Month', 'Day', 'Effective Federal Funds Rate'])
        #.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
        #.sort_values(by="Date")
    )
    
    """Turn the Year, Month, Day columns into a single date column that is properly formatted"""
    interest_data['Date'] = interest_data['Year'].astype(str) + '-' + interest_data['Month'].astype(str).str.zfill(2) + '-' + interest_data['Day'].astype(str).str.zfill(2)
    
    interest_data = interest_data.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")) #, inplace=True
    
    #print(interest_data.head())
    #print(type(interest_data['Date'][0]))
    #print(interest_data.tail())
    #print('---------------------')
    
    """The federal funds rate is the interest rate at which depository institutions trade federal funds 
    (balances held at Federal Reserve Banks) with each other overnight."""
    
    
    
    """Filling nan values with forward fill - this looks really bad for some reason"""
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    #interest_data = interest_data.ffill(axis=1)
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    
    
    """Filling nan values with mean - doesnt look great"""
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    #mean = interest_data['Effective Federal Funds Rate'].mean()
    #interest_data['Effective Federal Funds Rate'].fillna(value=mean, inplace=True)
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    
    """Filling nan values - this looks really bad for some reason"""
    print(interest_data['Effective Federal Funds Rate'].isna().sum())
    interest_data['Effective Federal Funds Rate'] = interest_data['Effective Federal Funds Rate'].ffill()
    print(interest_data['Effective Federal Funds Rate'].isna().sum())
    
    
    
    normalized_interest_rate = normalize_data(interest_data['Effective Federal Funds Rate'])
    interest_data['Effective Federal Funds Rate'] = normalized_interest_rate[0]
    
    
    interest_data.drop(columns=['Year', 'Month', 'Day'], inplace=True)
    
    #interest_data.rename(columns={"'Effective Federal Funds Rate'": "to_plot"})
    
    return interest_data








def get_house_supply_data():
    interest_data = (
        pd.read_csv("data/supply_of_new_houses.csv")
        .assign(Date=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
    
    #print(interest_data.head())
    #print(interest_data.tail())
    
    
    return interest_data



