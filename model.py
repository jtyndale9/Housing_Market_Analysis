# -*- coding: utf-8 -*-
"""
@author: chiragdhawan
"""

#from sklearn import preprocessing
import pandas as pd
import sys
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from datetime import date
from datetime import datetime

# Dictionary is keyed by date
def prepare_sp_500_dict(SP500_data):
    dict = {}
    for index, row in SP500_data.iterrows():
        dict[row['Date']] = row['Close*']
    return dict


# Dictionary is keyed by date
def prepare_interest_dict(interest_data):
    dict = {}
    for index, row in interest_data.iterrows():
        dict[row['Date']] = row['FEDFUNDS']
    return dict

# Dictionary is keyed by date
def prepare_house_supply_dict(house_supply_data):
    dict = {}
    for index, row in house_supply_data.iterrows():
        dict[row['Date']] = row['MSACSR']
    return dict

# Dictionary is keyed by date
def prepare_lumber_dict(lumber_data):
    dict = {}
    for index, row in lumber_data.iterrows():
        dict[row['Date']] = row['WPU081']
    return dict

# Dictionary is keyed by date
def prepare_hpi_dict(hpi_data):
    dict = {}
    for index, row in hpi_data.iterrows():
        dict[row['Date']] = row['USSTHPI_normalized']
    return dict

# Dictionary is keyed by date
def prepare_unemployment_dict(unemployment_data):
    dict = {}
    for index, row in unemployment_data.iterrows():
        dict[row['Date']] = row['Value']
    #print(dict)
    return dict



def get_data_for_specific_dates(dict, all_dates):
    data = []
    for date in all_dates:
        if(date in dict):
            data.append(dict[date])
        else:
            ## TODO(chiragdhawan) : Linear regression does not accept Null.
            # Think of possible way to handle ? Maybe drop rows with altogether ? But it may result in less data.
            data.append(-1)
    return data

def predict_top_features(checked_data_sources, SP500_data, interest_data, house_supply_data, lumber_data, hpi_data, unemployment_data, n):
    dict_sp500 = prepare_sp_500_dict(SP500_data)
    dict_interest = prepare_interest_dict(interest_data)
    dict_house_supply = prepare_house_supply_dict(house_supply_data)
    dict_lumber = prepare_lumber_dict(lumber_data)
    dict_hpi = prepare_hpi_dict(hpi_data)
    dict_unemployment = prepare_unemployment_dict(unemployment_data)
    ## Assuming that the hpi data is always present
    ## TODO(chirag): Think of what needs to be done where hpi data is not present
    all_dates = dict_hpi.keys()
    X = pd.DataFrame(index = all_dates)
    y = pd.DataFrame(index = all_dates)
    
    ## Prepare X
    for data_source in checked_data_sources:
        if(data_source == "S&P 500"):
            X['SP500'] = get_data_for_specific_dates(dict_sp500, all_dates)
        if(data_source == "Interest Rate"):
            X['Interest'] = get_data_for_specific_dates(dict_interest, all_dates)
        if(data_source == "Housing Supply"):
            X['House Supply'] = get_data_for_specific_dates(dict_house_supply, all_dates)
        if(data_source == "Lumber Prices"):
            X['Lumber'] = get_data_for_specific_dates(dict_lumber, all_dates)
        if(data_source == "Unemployment Rate"):
            X['Employment'] = get_data_for_specific_dates(dict_unemployment, all_dates)
    
    ## Prepare Y
    y['House Price Index'] = get_data_for_specific_dates(dict_hpi, all_dates)
    # print(X.head(5))
    # print(y.head(5))
    model = LinearRegression()
    model.fit(X, y)
    # get importance
    importance = model.coef_
    # print(importance)
    unsorted_dict = {}
    list_col = list(X.columns)
    for i,v in enumerate(importance[0]):
        unsorted_dict[v] = list_col[i]
        # print('Feature: %s, Score: %.5f' % (list_col[i],v))
    
    sorted_dict = sorted(unsorted_dict.items(), reverse=True)
    result = []
    score = []
    for item in sorted_dict:
         #print('Feature: %s, Score: %.5f' % (item[1],item[0]))
         result.append(item[1])
         score.append(item[0])
    return result[:n], score[:n]


def predict_future_values(checked_data_sources, SP500_data, interest_data, house_supply_data, lumber_data, hpi_data, unemployment_data):
    dict_sp500 = prepare_sp_500_dict(SP500_data)
    dict_interest = prepare_interest_dict(interest_data)
    dict_house_supply = prepare_house_supply_dict(house_supply_data)
    dict_lumber = prepare_lumber_dict(lumber_data)
    dict_hpi = prepare_hpi_dict(hpi_data)
    dict_unemployment = prepare_unemployment_dict(unemployment_data)
    ## Assuming that the hpi data is always present
    ## TODO(chirag): Think of what needs to be done where hpi data is not present
    all_dates = dict_hpi.keys()
    X = pd.DataFrame(index = all_dates)
    y = pd.DataFrame(index = all_dates)
    
    ## Prepare X
    for data_source in checked_data_sources:
        if(data_source == "S&P 500"):
            X['SP500'] = get_data_for_specific_dates(dict_sp500, all_dates)
        if(data_source == "Interest Rate"):
            X['Interest'] = get_data_for_specific_dates(dict_interest, all_dates)
        if(data_source == "Housing Supply"):
            X['House Supply'] = get_data_for_specific_dates(dict_house_supply, all_dates)
        if(data_source == "Lumber Prices"):
            X['Lumber'] = get_data_for_specific_dates(dict_lumber, all_dates)
        if(data_source == "Unemployment Rate"):
            X['Employment'] = get_data_for_specific_dates(dict_unemployment, all_dates)
    
    ## Prepare Y
    y['House Price Index'] = get_data_for_specific_dates(dict_hpi, all_dates)
    # print(X.head(5))
    # print(y.head(5))
    # print("Next is - ")

    # Drop the last row so that it look continous:
    last_element = y.iloc[-1]
    #print(last_element)
    y = y[:-1]
    model = ARIMA(y, order=(2,1,2))
    results = model.fit()
    # print(all_future_dates)
    # future_dates = []
    # for item in all_future_dates:
    #     future_dates.append(datetime.timestamp(item))
    # print(future_dates)
    forecast = results.forecast('2031-01-01')
    forecast[0] = last_element
    # print(forecast[0])
    all_values = forecast.values
    indexes = list(forecast.index.values)
    # print(all_values)
    # print(indexes)
    # print(forecast.head(10))
    # print(forecast.columns)
    return forecast


