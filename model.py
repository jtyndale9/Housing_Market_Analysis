# -*- coding: utf-8 -*-
"""
@author: chiragdhawan
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA


def monthly_series(data, column):
    """Index a series by date and average it to one value per month (handles daily S&P 500 data)."""
    return data.set_index('Date')[column].resample('MS').mean()


def predict_top_features(checked_data_sources, SP500_data, interest_data, house_supply_data, lumber_data, hpi_data, unemployment_data, n):
    """Rank the checked data sources by their linear regression coefficient against the HPI."""
    sources = {
        "S&P 500": ('SP500', SP500_data, 'Close*'),
        "Interest Rate": ('Interest', interest_data, 'FEDFUNDS'),
        "Housing Supply": ('House Supply', house_supply_data, 'MSACSR'),
        "Lumber Prices": ('Lumber', lumber_data, 'WPU081'),
        "Unemployment Rate": ('Employment', unemployment_data, 'Value'),
    }

    # HPI is quarterly, so the regression is fit on the HPI dates
    y = hpi_data.set_index('Date')['USSTHPI_normalized']
    X = pd.DataFrame(index=y.index)
    for data_source in checked_data_sources:
        if data_source in sources:
            name, data, column = sources[data_source]
            X[name] = monthly_series(data, column).reindex(y.index)

    if X.columns.empty:
        return ["N/A"], [0]

    # Drop dates where any selected indicator is missing rather than filling with a placeholder
    X = X.dropna()
    y = y.loc[X.index]

    model = LinearRegression()
    model.fit(X, y)

    ranked = sorted(zip(model.coef_, X.columns), reverse=True)
    result = [feature for _, feature in ranked]
    score = [coef for coef, _ in ranked]
    return result[:n], score[:n]


def predict_future_values(checked_data_sources, SP500_data, interest_data, house_supply_data, lumber_data, hpi_data, unemployment_data):
    """Forecast the national HPI through 2030 with an ARIMA(2,1,2) model."""
    y = hpi_data.set_index('Date')[['USSTHPI_normalized']]
    y.index = pd.DatetimeIndex(y.index, freq='QS')

    # Drop the last row so the forecast line connects to the historical line
    last_element = y.iloc[-1, 0]
    y = y[:-1]
    model = ARIMA(y, order=(2,1,2))
    results = model.fit()

    forecast = results.forecast('2031-01-01')
    forecast.iloc[0] = last_element
    return forecast
