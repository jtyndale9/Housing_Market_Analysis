# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:44:42 2023

@author: john4
"""

from sklearn import preprocessing
import pandas as pd
import sys
import numpy as np


START_YEAR = 1950
END_YEAR = 2023



def normalize_data(data):
    
    # This is returning different ranges of outputs....
    #normalized_data = preprocessing.normalize([data])
    
    #scaler = preprocessing.MinMaxScaler()
    #scaler.fit(data) # Compute the minimum and maximum to be used for later scaling.
    #scaler.transform(data) # Scale features of X according to feature_range.
    #return  scaler.transform(data)
    
    # By-hand calculation
    # zi = (xi – min(x)) / (max(x) – min(x)) * 100
    data = (data - min(data)) / (max(data) - min(data)) * 100
    #print("data before calculation: ")
    #print(data)
    #print("max data: ")
    #print(max(data))
    #print("min data: ")
    #print(min(data))
    
    return data
    



def get_sp500_data():
    SP500_data = (
        pd.read_csv("data/Federal/sp500_data.csv")
        .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
        .sort_values(by="Date")
    )
    
    #print(SP500_data.head())
    #print(SP500_data.columns)
    #print(SP500_data.tail())
    print(SP500_data.head())
    # Getting rid of the commas in the numbers for casting
    SP500_data['Close*'] = SP500_data['Close*'].str.replace(",", "")
    
    # Cast to float
    SP500_data['Close*'] = SP500_data['Close*'].astype(float)
    
    # Normalize data
    test = normalize_data(SP500_data['Close*'])
    SP500_data['Close*'] = test
    
    SP500_data.drop(columns=['Open', 'High', 'Low', 'Adj Close**', 'Volume'], inplace=True)
    
    #SP500_data.rename(columns={"Close*": "to_plot"})
    
    return SP500_data



def get_interest_rate_data():
    interest_data = (
        pd.read_csv("data/Federal/kaggle_fed_interest_rate_1954.csv", usecols = ['Year', 'Month', 'Day', 'Effective Federal Funds Rate'])
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
    
    """Filling nan values - this looks way better"""
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    interest_data['Effective Federal Funds Rate'] = interest_data['Effective Federal Funds Rate'].ffill()
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    
    normalized_interest_rate = normalize_data(interest_data['Effective Federal Funds Rate'])
    interest_data['Effective Federal Funds Rate'] = normalized_interest_rate
    
    interest_data.drop(columns=['Year', 'Month', 'Day'], inplace=True)
    
    #interest_data.rename(columns={"'Effective Federal Funds Rate'": "to_plot"})
    
    return interest_data








def get_house_supply_data():
    interest_data = (
        pd.read_csv("data/Federal/supply_of_new_houses.csv")
        .assign(DATE=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
        
    interest_data["MSACSR"] = normalize_data(interest_data['MSACSR'])
    
    interest_data.rename(columns={"DATE": "Date"}, inplace=True) # Rename DATE to Date for consistency
    
    # The months' supply indicates how long the current new for-sale inventory would last given the current sales rate if no additional new houses were built
    
    #print(interest_data.head())
    #print(interest_data.tail())
    
    return interest_data




def get_lumber_price_data():
    lumber_data = (
        pd.read_csv("data/Federal/WPU_wood_lumber_prices.csv")
        .assign(DATE=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
        
    lumber_data["WPU081"] = normalize_data(lumber_data['WPU081'])
    
    lumber_data.rename(columns={"DATE": "Date"}, inplace=True) # Rename DATE to Date for consistency
    
    #print(lumber_data.head())
    #print(lumber_data.tail())
    
    return lumber_data






def get_house_price_index_data():
    hpi_data = (
        pd.read_csv("data/Federal/Fed_house_price_index.csv")
        .assign(DATE=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
        
    hpi_data["USSTHPI"] = normalize_data(hpi_data['USSTHPI'])
    
    hpi_data.rename(columns={"DATE": "Date"}, inplace=True) # Rename DATE to Date for consistency
    
    #print(hpi_data.head())
    #print(hpi_data.tail())
    
    return hpi_data


def get_unemployment_data():
    unemployment_data = (
        pd.read_csv("data/Federal/federal_unemployment.csv")
        .assign(Date=lambda data: pd.to_datetime(data["Label"], format="%Y %b"))
        .sort_values(by="Date")
    )
    
    # Label - 1950 Jan
    # normalize Value
    
    unemployment_data["Value"] = normalize_data(unemployment_data['Value'])
    
    #unemployment_data.rename(columns={"Label": "Date"}, inplace=True) # Rename Label to Date for consistency
    
    unemployment_data.drop(columns={"Series ID", "Year", "Period", "Label"}, inplace=True)
    unemployment_data.reset_index(drop=True, inplace=True)
    print(unemployment_data.head())
    print(unemployment_data.tail())
    
    return unemployment_data










