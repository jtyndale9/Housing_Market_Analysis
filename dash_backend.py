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
#from dash import dcc
#from dash_html_template import Template

data = (
    pd.read_csv("sp500_data.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%d-%b-%y"))
    .sort_values(by="Date")
)


all_options =  ['S&P 500', 'Timber Prices', 'Unemployment', "Housing Supply", "Housing Costs"]

table_dict = {"Data Evaluated": "test", "Correlation Coefficient": 0.65}
table_array = ["Data Set 1", "Data Set 2", "Correlation Coefficient"]


print(data.head())


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
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
        
        
        
        # Drop Down div
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
                           options=['S&P 500', 'Timber Prices', 'Unemployment', "Housing Supply", "Housing Costs"],
                           value=['S&P 500']
                        )
                    ]
                ),
            ],
            className="menu",
        ),
        
        
        
            
        # inteactive visualization div
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
    
        # inteactive visualization div
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
def update_charts(data_type):
    price_chart_figure = {
        
        "data": [
            {
                "x": data["Date"],
                "y": data["Close*"],
                "type": "lines"
            },
        ],
        "layout": 
            {"title": { 
                    "text": f"{data_type}",
                    "x": 20,
                    "xanchor": "left"
                    },
             "xaxis": {"fixedrange": True},
             "yaxis": {"tickprefix": "$","fixedrange": True},
             "colorway": ["#17b897"]
            }
        }
    return price_chart_figure


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
    
    
    
    
    
    
    
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