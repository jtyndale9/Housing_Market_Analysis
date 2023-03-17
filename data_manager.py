# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:44:42 2023

@author: john4
"""

#from sklearn import preprocessing
import pandas as pd
import sys
import numpy as np
import datetime as dt


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

    
    return data
    



def get_sp500_data():
    SP500_data = (
        pd.read_csv("data/Federal/sp500_data.csv")
        .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
        .sort_values(by="Date")
    )
    
    
    # Getting rid of the commas in the numbers for casting
    SP500_data['Close*'] = SP500_data['Close*'].str.replace(",", "")
    
    # Cast to float
    SP500_data['Close*'] = SP500_data['Close*'].astype(float)
    
    # Normalize data
    test = normalize_data(SP500_data['Close*'])
    SP500_data['Close*'] = test
    
    SP500_data.drop(columns=['Open', 'High', 'Low', 'Adj Close**', 'Volume'], inplace=True)
    
    
    #SP500_data = SP500_data[SP500_data['Date'] > pd.Timestamp(1975,1,1)]
    SP500_data = SP500_data[(SP500_data['Date'] > dt.datetime(1974,12,31)) & ((SP500_data['Date'] < dt.datetime(2022,11,1)))] # Only include data after 1975
    SP500_data.reset_index(drop=True, inplace=True)
    
    return SP500_data



def get_interest_rate_data():
    interest_data = (
        pd.read_csv("data/Federal/FED_FUNDS_interest_rate.csv")
        .assign(Date=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="Date")
    )
    
    """Turn the Year, Month, Day columns into a single date column that is properly formatted"""
    #interest_data['Date'] = interest_data['Year'].astype(str) + '-' + interest_data['Month'].astype(str).str.zfill(2) + '-' + interest_data['Day'].astype(str).str.zfill(2)
    
    #interest_data = interest_data.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d")) #, inplace=True
    
    
    """The federal funds rate is the interest rate at which depository institutions trade federal funds 
    (balances held at Federal Reserve Banks) with each other overnight."""
    
    """Filling nan values with forward fill - this looks really bad for some reason"""
    #interest_data = interest_data.ffill(axis=1)
    
    
    """Filling nan values with mean - doesnt look great"""
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    #mean = interest_data['Effective Federal Funds Rate'].mean()
    #interest_data['Effective Federal Funds Rate'].fillna(value=mean, inplace=True)
    
    """Filling nan values - this looks way better"""
    #print(interest_data['Effective Federal Funds Rate'].isna().sum())
    #interest_data['Effective Federal Funds Rate'] = interest_data['Effective Federal Funds Rate'].ffill()
    
    normalized_interest_rate = normalize_data(interest_data['FEDFUNDS'])
    interest_data['FEDFUNDS'] = normalized_interest_rate
    
    interest_data.drop(columns=['DATE'], inplace=True)
    
    interest_data = interest_data[(interest_data['Date'] > dt.datetime(1974,12,31)) & ((interest_data['Date'] < dt.datetime(2022,11,1)))]
    interest_data.reset_index(drop=True, inplace=True)
    
    return interest_data








def get_house_supply_data():
    house_supply_data = (
        pd.read_csv("data/Federal/supply_of_new_houses.csv")
        .assign(DATE=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
        
    house_supply_data["MSACSR"] = normalize_data(house_supply_data['MSACSR'])
    
    house_supply_data.rename(columns={"DATE": "Date"}, inplace=True) # Rename DATE to Date for consistency
    
    # The months' supply indicates how long the current new for-sale inventory would last given the current sales rate if no additional new houses were built
    
    house_supply_data = house_supply_data[(house_supply_data['Date'] > dt.datetime(1974,12,31))  & ((house_supply_data['Date'] < dt.datetime(2022,11,1)))]
    house_supply_data.reset_index(drop=True, inplace=True)
    
    return house_supply_data




def get_lumber_price_data():
    lumber_data = (
        pd.read_csv("data/Federal/WPU_wood_lumber_prices.csv")
        .assign(DATE=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
        
    lumber_data["WPU081"] = normalize_data(lumber_data['WPU081'])
    
    lumber_data.rename(columns={"DATE": "Date"}, inplace=True) # Rename DATE to Date for consistency
    
    lumber_data = lumber_data[(lumber_data['Date'] > dt.datetime(1974,12,31)) & ((lumber_data['Date'] < dt.datetime(2022,11,1)))]
    lumber_data.reset_index(drop=True, inplace=True)
    
    return lumber_data






def get_house_price_index_data():
    hpi_data = (
        pd.read_csv("data/Federal/Fed_house_price_index.csv")
        .assign(DATE=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m-%d"))
        .sort_values(by="DATE")
    )
        
    hpi_data["USSTHPI"] = normalize_data(hpi_data['USSTHPI'])
    
    hpi_data.rename(columns={"DATE": "Date"}, inplace=True) # Rename DATE to Date for consistency
    
    hpi_data = hpi_data[(hpi_data['Date'] > dt.datetime(1974,12,31)) & ((hpi_data['Date'] < dt.datetime(2022,11,1)))]
    hpi_data.reset_index(drop=True, inplace=True)
    
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
    
    unemployment_data = unemployment_data[(unemployment_data['Date'] > dt.datetime(1974,12,31))  & ((unemployment_data['Date'] < dt.datetime(2022,11,1)))]
    unemployment_data.reset_index(drop=True, inplace=True)
    
    return unemployment_data





def get_correlation_dataframe():
    
    # n(n-1) / 2 is the amount of unique combinations
    
    data_sets_col_a = ["hpi_data", "hpi_data", "hpi_data", "hpi_data", "hpi_data", 
                 "SP500_data", "SP500_data", "SP500_data", "SP500_data", 
                 "lumber_data", "lumber_data", "lumber_data", 
                 "unemployment_data", "unemployment_data", 
                 "house_supply_data"]
    
    data_sets_col_b = ["SP500_data", "lumber_data", "unemployment_data", "house_supply_data", "interest_data",
                        "lumber_data", "unemployment_data", "house_supply_data", "interest_data",
                        "unemployment_data", "house_supply_data", "interest_data",
                        "house_supply_data", "interest_data",
                        "interest_data"]
    
    correlations = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    
    
    #correlation_test_a = np.corrcoef(x, y)
    hpi = get_house_price_index_data() #["USSTHPI"]
    sp500 = get_sp500_data() #['Close*']
    unemployment = get_unemployment_data()
    lumber = get_lumber_price_data()
    supply = get_house_supply_data()
    interest = get_interest_rate_data()
    
    
    """Resampling HPI data so that it is the same length as the other data.
       Changing from one data point per quarter to one data point per month
       forward filling the data"""
    # HPI data is sampled every quarter. so 4 data points per year.
    hpi = hpi.set_index('Date')
    hpi = hpi.resample('MS').ffill()
    hpi['Date'] = hpi.index
    hpi.reset_index(drop=True, inplace=True)
    
    """Resample for once a month, using the mean."""
    sp500 = sp500.set_index('Date')
    sp500 = sp500.resample('MS').mean()
    sp500['Date'] = sp500.index
    sp500.reset_index(drop=True, inplace=True)
    
    print('-----------correlations-------------')
    
    correlation_df = pd.DataFrame({"hpi": hpi['USSTHPI'], "sp500": sp500['Close*'], "unemployment": unemployment['Value'], "lumber": lumber["WPU081"], "supply": supply['MSACSR'], "interest": interest['FEDFUNDS'] })
    correlations_df = correlation_df.corr()
    print(correlations_df)
    
    
    
    correlations[0] = round(correlation_df['hpi'].corr(correlation_df['sp500']), 4)
    correlations[1] = round(correlation_df['hpi'].corr(correlation_df['lumber']), 4)
    correlations[2] = round(correlation_df['hpi'].corr(correlation_df['unemployment']), 4)
    correlations[3] = round(correlation_df['hpi'].corr(correlation_df['supply']), 4)
    correlations[4] = round(correlation_df['hpi'].corr(correlation_df['interest']), 4)
    
    correlations[5] = round(correlation_df['sp500'].corr(correlation_df['lumber']), 4)
    correlations[6] = round(correlation_df['sp500'].corr(correlation_df['unemployment']), 4)
    correlations[7] = round(correlation_df['sp500'].corr(correlation_df['supply']), 4)
    correlations[8] = round(correlation_df['sp500'].corr(correlation_df['interest']), 4)
    
    correlations[9] = round(correlation_df['lumber'].corr(correlation_df['unemployment']), 4)
    correlations[10] = round(correlation_df['lumber'].corr(correlation_df['supply']), 4)
    correlations[11] = round(correlation_df['lumber'].corr(correlation_df['interest']), 4)
    
    correlations[12] = round(correlation_df['unemployment'].corr(correlation_df['supply']), 4)
    correlations[13] = round(correlation_df['unemployment'].corr(correlation_df['interest']), 4)
    
    correlations[14] = round(correlation_df['supply'].corr(correlation_df['interest']), 4)
    #print(correlations)
    
    
    
    
    hpi_sp500_correlation = np.corrcoef(hpi["USSTHPI"], sp500['Close*'])
    print(hpi_sp500_correlation)
    
    
    #table_df["Data Set 1"] = data_sets_col_a
    #table_df["Data Set 2"] = data_sets_col_b
    #table_df["Correlation Coefficient"] = correlations
    
    table_df = pd.DataFrame({"Data_Set_1": data_sets_col_a, "Data_Set_2": data_sets_col_b, "Correlation_Coefficient": correlations})
    #print(table_df.head())
    #print(table_df.columns)
    #table_df = pd.DataFrame(columns=["Data Set 1", "Data Set 2", "Correlation Coefficient"])
    
    return table_df


















