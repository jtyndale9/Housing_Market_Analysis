# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:04:57 2023

@author: e417027
"""

# app.py

import pandas as pd
from dash import Dash, dcc, html
import dash_core_components as dcc
from dash import Input, Output
from dash import dash_table
import datetime
import plotly.graph_objects as go

#from dash import dcc
#from dash_html_template import Template


import data_manager


# Filter options
all_options =  ["hpi_data", "SP500_data", "lumber_data", "unemployment_data", "house_supply_data", "interest_data"]

# Dummy data to fill the table
table_dict = {"Data Evaluated": "test", "Correlation Coefficient": 0.65}
table_array = ["Data Set 1", "Data Set 2", "Correlation Coefficient"]



"""Import all data here"""
SP500_data = data_manager.get_sp500_data()
interest_data = data_manager.get_interest_rate_data()
house_supply_data = data_manager.get_house_supply_data()
lumber_data = data_manager.get_lumber_price_data()
hpi_data = data_manager.get_house_price_index_data()
unemployment_data = data_manager.get_unemployment_data()



"""Merging data here... may or may not use"""
# Place the DataFrames side by side
combined_data = pd.concat([SP500_data, interest_data], axis=1)
#print(combined_data.head())
joined_data = SP500_data.merge(interest_data, on='Date') #, how='inner'
#print(joined_data.head())
#print(joined_data.columns)


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    }
]


app = Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(
    children=[
        
        
        
        # Header div
        html.Div(
            children=[
                html.P(
                    children="Data & Visual Analytics: Spring 2023 Project",
                    className="header-description"
                ),
                html.H1(children="Correlations of Housing Prices",
                        className='header-title'),
                html.P(
                    children="Joshua Tyndale, Chirag Dhawan, Timothy Lee, Yu-Xi Chen, Manasa Kumashi, Nikolos Lahanis",
                    className="names"
                ),
                        #style={"color": "#CFCFCF", "margin": "4px auto", "text-align": "center", "max-width": "384px"}),
            ],
            className="header"
        ),
        
        
        
        # Filter check box div
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="", className="menu-title"),
                        #dcc.Dropdown(
                        #    id='countries-dropdown',
                        #    options=[k for k in all_options],
                        #    value='S&P 500',
                        #    clearable=False,
                        #    className="dropdown",
                        #    multi=True
                        #),
                        dcc.Checklist(
                           id="select-checklist",
                           options=all_options,
                           value=["hpi_data", "SP500_data", "interest_data", "house_supply_data", "lumber_data", "unemployment_data"]
                        )
                    ]
                ),
            ],
            className="menu",
        ),
        
    
    
        # inteactive line plot visualization div
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart-2",
                        config={"displayModeBar": False}, # remove the floating toolbar that Plotly shows by default.
                        className="card",
                    ),
                className="wrapper",
                )
                
            ]
        ),
    
    
    
        # table  div
        html.Div(
            children=[
                html.Div(
                    children=dash_table.DataTable(columns=[{
                                                    'name': table_array[i],
                                                    'id': 'column-{}'.format(i)
                                                           } for i in range(len(table_array))] ,
                                                 data=[
                                                    {'column-0': "Example A: (S&P 500)",'column-1': "Example B: (Timber Prices)",'column-2': "Example: 56.5%"}
                                                 ]
                                                 #data=[
                                                 #   {'column-{}'.format(i): (j + (i-1)*5) for i in range(0, 3)}
                                                 #   for j in range(5)
                                                 #]
                                                 ),
                                                className="wrapper",
                )
            ]
        )
    ]
)





@app.callback(
    Output("price-chart-2", "figure"),
    Input("select-checklist", "value")
)
def update_charts(checked_data_sources):
    
    """This dynamically adds a new line for each data source checked on the gui"""
    line_plots = []
    for i in range(len(checked_data_sources)):
        if(checked_data_sources[i] == "SP500_data"):
            line_plots.append(go.Scatter(
                {
                    "x": SP500_data["Date"], 
                    "y": SP500_data["Close*"], 
                    "type": "lines",
                    "name": "S&P 500",
                    "line": dict(color="red")
                    
                }))
        if(checked_data_sources[i] == "interest_data"):
            line_plots.append(go.Scatter(
                {
                    "x": interest_data["Date"],
                    "y": interest_data["Effective Federal Funds Rate"],  
                    "type": "lines",
                    "name": "Fed Interest Rate",
                    "line": dict(color="blue")
                }))
        if(checked_data_sources[i] == "house_supply_data"):
            line_plots.append(go.Scatter(
                {
                    "x": house_supply_data["Date"],
                    "y": house_supply_data["MSACSR"], 
                    "type": "lines",
                    "name": "House Supply -MSACSR",
                    "line": dict(color="orange")
                }))
        if(checked_data_sources[i] == "lumber_data"):
            line_plots.append(go.Scatter(
                {
                    "x": lumber_data["Date"],
                    "y": lumber_data["WPU081"], 
                    "type": "lines",
                    "name": "lumber_data",
                    "line": dict(color="purple")
                }))
            
        if(checked_data_sources[i] == "hpi_data"):
            line_plots.append(go.Scatter(
                {
                    "x": hpi_data["Date"],
                    "y": hpi_data["USSTHPI"], 
                    "type": "lines",
                    "name": "hpi_data",
                    "line": dict(color="black")
                }))
        if(checked_data_sources[i] == "unemployment_data"):
            line_plots.append(go.Scatter(
                {
                    "x": unemployment_data["Date"],
                    "y": unemployment_data["Value"], 
                    "type": "lines",
                    "name": "unemployment_data",
                    "line": dict(color="green")
                }))
        # unemployment_data
            
    """This returns the figure on update"""
    price_chart_figure = {
        "data": line_plots, # Set data equal to line plot data array defined above
        
        "layout": 
            {"title": { 
                    "text": f"{checked_data_sources}",
                    "x": 20
                    #"xanchor": "left"
                    },
             "xaxis": {"fixedrange": True},
             "yaxis": {
                 #"tickprefix": "$",
                 "fixedrange": True,
                 'showticklabels': False},
             "colorway": ["#17b897"]
            }
        }
    return price_chart_figure












if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    """
            "data": [go.Scatter(
            {
                "x": SP500_data["Date"],  #, house_supply_data['DATE']
                "y": SP500_data["Close*"],  #, house_supply_data['MSACSR']
                "type": "lines",
                "name": "S&P 500"
            },
        ),
            go.Scatter(
            {
                "x": interest_data["Date"],  #, house_supply_data['DATE']
                "y": interest_data["Effective Federal Funds Rate"],  #, house_supply_data['MSACSR']
                "type": "lines",
                "name": "Interest Rates",
                "fill": "none",  # ['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx','toself', 'tonext']
                "line": dict(color="red")
            },
                )
            ],
    """
    
    
    """
            # visualization div
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False}, # remove the floating toolbar that Plotly shows by default.
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Close*"],
                                    "type": "lines"
                                },
                            ],
                            "layout": 
                                {"title": { 
                                        "text": "S&P 500 Closes",
                                        "x": 20,
                                        #"text-align": "center",
                                        "xanchor": "left"
                                        },
                                 "xaxis": {"fixedrange": True},
                                 "yaxis": {"tickprefix": "$","fixedrange": True},
                                 "colorway": ["#17b897"]
                                }
                        },
                        className="card",
                    ),
                className="wrapper",
                )
            ]
        ),
    """