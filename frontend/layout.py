# """This script defines the layout for the Dash frontend, which includes a title, a dropdown for filtering violation types (with options like "All" or "Speed Violation"), and a map visualization to display vehicle violations. It also includes a data table that shows detailed information about each violation, such as license plate, speed, latitude, longitude, and timestamp, with pagination set to display 10 records per page. The map and table are connected to the backend data and dynamically updated based on user input."""

# # frontend/layout.py
# from dash import dcc
# from dash import html
# from dash import dash_table
# from dash import dash_table

# layout = html.Div([
#     html.H1("Vehicle Violation Dashboard"),
    
#     # Dropdown or filter section if needed
#     dcc.Dropdown(
#         id='violation-filter',
#         options=[
#             {'label': 'All', 'value': 'ALL'},
#             {'label': 'Speed Violation', 'value': 'SPEED'},
#         ],
#         value='ALL',
#         clearable=False,
#     ),
    
#     # Map Section to show violations on map
#     dcc.Graph(id='map-visualization'),

#     # Table to show the violation list
#     dash_table.DataTable(
#         id='violation-table',
#         columns=[
#             {"name": "License Plate", "id": "license_plate"},
#             {"name": "Speed", "id": "speed"},
#             {"name": "Latitude", "id": "latitude"},
#             {"name": "Longitude", "id": "longitude"},
#             {"name": "Timestamp", "id": "timestamp"}
#         ],
#         page_size=10
#     ),
# ])


# frontend/layout.py
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table


# Define the layout
layout = dbc.Container([

    # Title
    dbc.Row(
        dbc.Col(
            html.H1("Vehicle Violation Dashboard", className="text-center my-5"),
            width=12
        )
    ),
    
    # Dropdown or filter section
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id='violation-filter',
                options=[
                    {'label': 'All Violations', 'value': 'ALL'},
                    {'label': 'Speed Violation', 'value': 'SPEED'},
                ],
                value='ALL',  # Default value
                clearable=False,
                className="mb-4",
                style={"width": "50%", "margin": "auto"}  # Center the dropdown
            ),
            width=12
        )
    ),
    
    # Map Section to show violations on the map
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='map-visualization'),  # Graph component for map visualization
            width=12
        )
    ),
    
    # Table to show the violation list
    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
                id='violation-table',
                columns=[
                    {"name": "License Plate", "id": "license_plate"},
                    {"name": "Speed", "id": "speed"},
                    {"name": "Latitude", "id": "latitude"},
                    {"name": "Longitude", "id": "longitude"},
                    {"name": "Timestamp", "id": "timestamp"}
                ],
                page_size=10,
                style_table={'height': '300px', 'overflowY': 'auto'},  # Add scrollable table if needed
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                },
            ),
            width=12
        )
    ),
], fluid=True)  # Make the layout responsive

