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
import matplotlib.pyplot as plt


START_YEAR = 1950
END_YEAR = 2023

state_map = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California',
             'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
             'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
             'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
             'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
             'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina',
             'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
             'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
             'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
             'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
             'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

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
    

def get_rental_data():
    rental_data = (
        pd.read_csv("data/Federal/Rent_Prices.csv")
        .assign(Date=lambda data: pd.to_datetime(data["observation_date"], format="%m/%d/%Y")) #%d/%b/%Y
        .sort_values(by="Date")
    )
    rental_data = rental_data[['Date', 'CUSR0000SEHA']]
    #print(rental_data)
    rental_data['CUSR0000SEHA'] = normalize_data(rental_data['CUSR0000SEHA'])
    rental_data = rental_data[(rental_data['Date'] > dt.datetime(1974,12,31)) & ((rental_data['Date'] < dt.datetime(2022,11,1)))]
    return rental_data


def get_savings_data():
    savings_data = (
        pd.read_csv("data/Federal/Personal_Savings_Rate.csv")
        .assign(Date=lambda data: pd.to_datetime(data["observation_date"], format="%m/%d/%Y"))
        .sort_values(by="Date")
    )
    savings_data = savings_data[['Date', 'PSAVERT']]
    #print(savings_data)
    savings_data['PSAVERT'] = normalize_data(savings_data['PSAVERT'])
    savings_data = savings_data[(savings_data['Date'] > dt.datetime(1974,12,31)) & ((savings_data['Date'] < dt.datetime(2022,11,1)))]
    return savings_data



def get_rental_vac_data():
    rental_vac_data = (
        pd.read_csv("data/Federal/Rental_Vacancies.csv")
        .assign(Date=lambda data: pd.to_datetime(data["observation_date"], format=r"%m/%d/%Y"))
        .sort_values(by="Date")
    )
    rental_vac_data = rental_vac_data[['Date', 'RRVRUSQ156N']]
    #print(rental_vac_data)
    rental_vac_data['RRVRUSQ156N'] = normalize_data(rental_vac_data['RRVRUSQ156N'])
    rental_vac_data = rental_vac_data[(rental_vac_data['Date'] > dt.datetime(1974,12,31)) & ((rental_vac_data['Date'] < dt.datetime(2022,11,1)))]
    return rental_vac_data

def get_labor_part_data():
    labor_part_data = (
        pd.read_csv("data/Federal/Labor_Force_Participation.csv")
        .assign(Date=lambda data: pd.to_datetime(data["observation_date"], format="%m/%d/%Y"))
        .sort_values(by="Date")
    )
    labor_part_data = labor_part_data[['Date', 'CIVPART']]
    #print(labor_part_data)
    labor_part_data['CIVPART'] = normalize_data(labor_part_data['CIVPART'])
    labor_part_data = labor_part_data[(labor_part_data['Date'] > dt.datetime(1974,12,31)) & ((labor_part_data['Date'] < dt.datetime(2022,11,1)))]
    return labor_part_data

def get_cpi_data():
    cpi_data = (
        pd.read_excel("data/Federal/Consumer_Price_Index.xlsx")
        .assign(Date=lambda data: pd.to_datetime(data["observation_date"], format="%Y-%m-%d"))
        .sort_values(by="Date")
    )
    cpi_data = cpi_data[['Date', 'CPIAUCSL']]
    #print(cpi_data)
    cpi_data['CPIAUCSL'] = normalize_data(cpi_data['CPIAUCSL'])
    cpi_data = cpi_data[(cpi_data['Date'] > dt.datetime(1974,12,31)) & ((cpi_data['Date'] < dt.datetime(2022,11,1)))]
    return cpi_data



def get_permit_data():
    permit_data = (
        pd.read_excel("data/Federal/Building_permits.xlsx")
        .assign(Date=lambda data: pd.to_datetime(data["Year"], format="%Y"))
        .sort_values(by="Date")
    )
    permit_data = permit_data[['Date', 'Total']]
    
    permit_data['Total'] = normalize_data(permit_data['Total'])
    
    permit_data = permit_data[(permit_data['Date'] > dt.datetime(1974,12,31)) & ((permit_data['Date'] < dt.datetime(2022,11,1)))]
    
    return permit_data


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
        
    hpi_data["USSTHPI_normalized"] = normalize_data(hpi_data['USSTHPI'])

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


def get_home_ownership_data():
    home_ownership_data = (
        pd.read_csv("data/Federal/federal_unemployment.csv")
            .assign(Date=lambda data: pd.to_datetime(data["Label"], format="%Y %b"))
            .sort_values(by="Date")
    )

"""State Data"""

start_date = dt.datetime(1974, 12, 31)
end_date = dt.datetime(2022, 11, 1)

def convert_to_datetime(date_str):
    year, quarter = date_str.split(':')
    quarter_num = int(quarter[-1])
    month = ((quarter_num - 1) * 3) + 1
    date = dt.datetime(int(year), month, 1)
    return date

def personal_income_state():

    # Read the CSV file while skipping the first 3 rows and last 5 rows
    personal_income = pd.read_csv("data/State/Personal_income.csv",skiprows=3, skipfooter=5, engine='python')

    personal_income.drop(columns=['GeoFips'], inplace=True)
    personal_income.rename(columns={'GeoName': 'state'}, inplace=True)
    personal_income = pd.melt(personal_income, id_vars=['state'], var_name='Date', value_name='value')
    personal_income = personal_income[personal_income['value'] != '(NA)']
    personal_income.iloc[:, 1] = personal_income.iloc[:, 1].apply(convert_to_datetime)
    personal_income['value'] = pd.to_numeric(personal_income['value'])
    personal_income["value"] = normalize_data(personal_income['value'])
    personal_income = personal_income[(personal_income['Date'] > start_date) & (personal_income['Date'] < end_date)]
    personal_income.reset_index(drop=True, inplace=True)

    return personal_income

def load_data(state_code):

    #Couldn't find DC data
    if state_code == 'DC' :
        return

    unemployment_data = pd.read_csv("data/State/Unemployment_rate/" + state_code + "_Unemployment.csv")

    unemployment_data["Date"] = pd.to_datetime(unemployment_data["Label"], format="%Y %b")
    unemployment_data.sort_values(by="Date", inplace=True)
    # Drop unnecessary columns
    unemployment_data = unemployment_data.drop(columns=["Series ID", "Year", "Label", "Period"])

    # Normalize Value
    unemployment_data["Value"] = normalize_data(unemployment_data["Value"])

    # Filter data by date
    unemployment_data = unemployment_data[
        (unemployment_data["Date"] > start_date) & (unemployment_data["Date"] < end_date)]

    # Reset index
    unemployment_data.reset_index(drop=True, inplace=True)
    # unemployment_data.to_csv("data/State/unemp_state.csv", index=False)
    return unemployment_data
# data = load_data('CA')
# print("data",data)

def unemployment_data():
    # Returns a map from state code (string) to datafarme for unemp data for that state.
    unemp_data_per_state = {}
    for key,value in state_map.items():
        unemp_data_per_state[state_map[key]] = load_data(key)
        # print(unemp_data_per_state[key])
    return unemp_data_per_state

def load_data_hpi(state_code):

    #Testing CA and FL (yet to add other data)
    # if state_code != 'CA':
    #     return

    hpi_data_state = pd.read_csv("data/State/HPI_state_data/" + state_code + "STHPI.csv")
    hpi_data_state["Date"] = pd.to_datetime(hpi_data_state["DATE"], format="%Y-%m-%d")
    hpi_data_state.rename(columns={hpi_data_state.columns[1]: 'hpi'}, inplace=True)
    hpi_data_state.sort_values(by="Date", inplace=True)

    hpi_data_state["hpi"] = normalize_data(hpi_data_state["hpi"])

    # Filter data by date
    hpi_data_state = hpi_data_state[
        (hpi_data_state["Date"] > start_date) & (hpi_data_state["Date"] < end_date)]

    # Reset index
    hpi_data_state.reset_index(drop=True, inplace=True)
    return hpi_data_state


def hpi_data_state():
    hpi_data_per_state = {}
    for key, value in state_map.items():
        hpi_data_per_state[state_map[key]] = load_data_hpi(key)
    return hpi_data_per_state

# def  load_housing_permit_data(state_code):
#
#     housing_permits = pd.read_csv("data/State/Private_Housing_unit_permit/" + state_code + "BPPRIVSA.csv")
#     housing_permits["Date"] = pd.to_datetime(housing_permits["DATE"], format="%Y-%m-%d")
#
#     housing_permits.drop(columns=["DATE"], inplace=True)
#     housing_permits.rename(columns={housing_permits.columns[1]: 'value'}, inplace=True)
#     housing_permits.sort_values(by="Date", inplace=True)
#     # print(housing_permits["value"].dtype)
#
#     # housing_permits["value"] = normalize_data(housing_permits["value"])
#
#     # Filter data by date
#     housing_permits = housing_permits[
#         (housing_permits["Date"] > start_date) & (housing_permits["Date"] < end_date)]
#
#     # Reset index
#
#     housing_permits.reset_index(drop=True, inplace=True)
#     print(housing_permits.head())
#
#     return housing_permits
#
# def housing_permits_state():
#     # Returns a map from state code (string) to datafarme for unemp data for that state.
#     housing_permits_state = {}
#     for key,value in state_map.items():
#         housing_permits_state[state_map[key]] = load_housing_permit_data(key)
#         # print(unemp_data_per_state[key])
#     return housing_permits_state

def  load_min_wage_rate(state_code):
    if state_code == 'AL' or  state_code == 'LA' or  state_code == 'TN' or state_code == 'MS' or state_code == 'SC':
        return

    min_wage_data = pd.read_csv("data/State/Min_wage_rate/STTMINWG" + state_code + ".csv")
    min_wage_data["Date"] = pd.to_datetime(min_wage_data["DATE"], format="%Y-%m-%d")
    min_wage_data.rename(columns={min_wage_data.columns[1]: 'value'}, inplace=True)
    min_wage_data.sort_values(by="Date", inplace=True)

    min_wage_data["value"] = normalize_data(min_wage_data["value"])

    # Filter data by date
    min_wage_data = min_wage_data[
        (min_wage_data["Date"] > start_date) & (min_wage_data["Date"] < end_date)]

    # Reset index
    min_wage_data.reset_index(drop=True, inplace=True)
    return min_wage_data

def min_wage_rate():
    # Returns a map from state code (string) to datafarme for unemp data for that state.

    min_wage_rate = {}
    for key,value in state_map.items():
        min_wage_rate[state_map[key]] = load_min_wage_rate(key)
        # print(unemp_data_per_state[key])
    return min_wage_rate

def  load_rental_vacancy_rate(state_code):
    if state_code == 'KY':
        return
    rental_vacancy_data = pd.read_csv("data/State/Rental_vacancy_rate/" + state_code + "RVAC.csv")
    rental_vacancy_data["Date"] = pd.to_datetime(rental_vacancy_data["DATE"], format="%Y-%m-%d")
    rental_vacancy_data.rename(columns={rental_vacancy_data.columns[1]: 'value'}, inplace=True)
    rental_vacancy_data.sort_values(by="Date", inplace=True)

    rental_vacancy_data["value"] = normalize_data(rental_vacancy_data["value"])

    # Filter data by date
    rental_vacancy_data = rental_vacancy_data[
        (rental_vacancy_data["Date"] > start_date) & (rental_vacancy_data["Date"] < end_date)]

    # Reset index
    rental_vacancy_data.reset_index(drop=True, inplace=True)
    return rental_vacancy_data

def rental_vacancy_rate():
    # Returns a map from state code (string) to datafarme for unemp data for that state.
    rental_vacancy_rate = {}
    for key,value in state_map.items():
        rental_vacancy_rate[state_map[key]] = load_rental_vacancy_rate(key)
        # print(unemp_data_per_state[key])
    return rental_vacancy_rate

"""End state data"""
# data = housing_permits_state()





def get_correlation_to_hpi():
    
    hpi = ["Housing Price Index"]
    data_sets_col_a = hpi * 11
    
    data_sets_col_b = ["S&P 500", 
                       "Lumber Prices",
                       "Unemployment Rate", 
                       "Housing Supply", 
                       "Interest Rate",
                       "Building Permits",
                       "Consumer Price Index",
                       "Rent Prices",
                       "Savings",
                       "Rental Vacancies",
                       "Labor Participation"]
    
    correlations = [1,2,3,4,5,6,7,8,9,10,11]
    
    hpi = get_house_price_index_data() #["USSTHPI"]
    sp500 = get_sp500_data() #['Close*']
    unemployment = get_unemployment_data()
    lumber = get_lumber_price_data()
    supply = get_house_supply_data()
    interest = get_interest_rate_data()
    permit_data = get_permit_data()
    cpi_data = get_cpi_data()
    rental_data = get_rental_data()
    savings_data = get_savings_data()
    rental_vacancies_data = get_rental_vac_data()
    labor_participation_data = get_labor_part_data()
    
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
    
    """Resample permit data"""
    permit_data = permit_data.set_index('Date')
    permit_data = permit_data.resample('MS').ffill()
    permit_data['Date'] = permit_data.index
    permit_data.reset_index(drop=True, inplace=True)
    fill = pd.DataFrame({'Date': pd.date_range(dt.datetime(2022,1,1), dt.datetime(2022,10,1), freq='M')})
    fill['Total'] = [65] * 9
    permit_data = permit_data.append(fill)
    permit_data.reset_index(drop=True, inplace=True)
    
    """Fill in missing dates"""
    fill = pd.DataFrame({'Date': pd.date_range(dt.datetime(1975,1,1), dt.datetime(1980,12,31), freq='M')})
    fill['CUSR0000SEHA'] = [0] * 72
    rental_data = fill.append(rental_data)
    rental_data.reset_index(drop=True, inplace=True)
    
    """Resample rental vacancy data"""
    rental_vacancies_data = rental_vacancies_data.set_index('Date')
    rental_vacancies_data = rental_vacancies_data.resample('MS').ffill()
    rental_vacancies_data['Date'] = rental_vacancies_data.index
    rental_vacancies_data.reset_index(drop=True, inplace=True)
    
    
    correlation_df = pd.DataFrame({"Housing Price Index": hpi['USSTHPI_normalized'], 
                                   "S&P 500": sp500['Close*'], 
                                   "Unemployment Rate": unemployment['Value'], 
                                   "Lumber Prices": lumber["WPU081"], 
                                   "Housing Supply": supply['MSACSR'], 
                                   "Interest Rate": interest['FEDFUNDS'],
                                   
                                   "Building Permits": permit_data['Total'], 
                                   "Consumer Price Index": cpi_data['CPIAUCSL'], 
                                   "Rent Prices": rental_data['CUSR0000SEHA'], 
                                   "Savings": savings_data['PSAVERT'], 
                                   "Rental Vacancies": rental_vacancies_data['RRVRUSQ156N'], 
                                   "Labor Participation": labor_participation_data['CIVPART']})
    
    correlations_df = correlation_df.corr()

    
    for i, item in enumerate(data_sets_col_a):
        correlations[i] = round(correlation_df[data_sets_col_a[i]].corr(correlation_df[data_sets_col_b[i]]), 4)
        
    table_df = pd.DataFrame({"Data_Set_1": data_sets_col_a, "Data_Set_2": data_sets_col_b, "Correlation_Coefficient": correlations})
    print(table_df)
    return table_df

def get_correlation_dataframe():
    
    # n(n-1) / 2 is the amount of unique combinations
    
    data_sets_col_a = ["Housing Price Index", "Housing Price Index", "Housing Price Index", "Housing Price Index", "Housing Price Index", 
                 "S&P 500", "S&P 500", "S&P 500", "S&P 500", 
                 "Lumber Prices", "Lumber Prices", "Lumber Prices", 
                 "Unemployment Rate", "Unemployment Rate", 
                 "Housing Supply"]
    
    data_sets_col_b = ["S&P 500", "Lumber Prices", "Unemployment Rate", "Housing Supply", "Interest Rate",
                        "Lumber Prices", "Unemployment Rate", "Housing Supply", "Interest Rate",
                        "Unemployment Rate", "Housing Supply", "Interest Rate",
                        "Housing Supply", "Interest Rate",
                        "Interest Rate"]

    
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
    
    #print('-----------correlations-------------')
    
    correlation_df = pd.DataFrame({"Housing Price Index": hpi['USSTHPI'], 
                                   "S&P 500": sp500['Close*'], 
                                   "Unemployment Rate": unemployment['Value'], 
                                   "Lumber Prices": lumber["WPU081"], 
                                   "Housing Supply": supply['MSACSR'], 
                                   "Interest Rate": interest['FEDFUNDS'] })
    
    #correlations_df = correlation_df.corr()
    #print(correlations_df)
    
    
    for i, item in enumerate(data_sets_col_a):
        correlations[i] = round(correlation_df[data_sets_col_a[i]].corr(correlation_df[data_sets_col_b[i]]), 4)
    

    #hpi_sp500_correlation = np.corrcoef(hpi["USSTHPI"], sp500['Close*'])
    #print(hpi_sp500_correlation)
    
    
    #table_df["Data Set 1"] = data_sets_col_a
    #table_df["Data Set 2"] = data_sets_col_b
    #table_df["Correlation Coefficient"] = correlations
    #print(hpi_sp500_correlation)
    
    table_df = pd.DataFrame({"Data_Set_1": data_sets_col_a, "Data_Set_2": data_sets_col_b, "Correlation_Coefficient": correlations})

    return table_df


















