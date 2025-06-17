# """This script defines a callback function for updating the map visualization and violation table based on a selected filter value. It fetches violation data from the backend API, filters it according to the selected filter (if any), and then updates the map and table with the relevant data. The map is generated using Plotly's scatter_mapbox, displaying violations based on latitude and longitude, and the table shows details like license plates, speed, and timestamps."""

# # frontend/callbacks.py
# from dash import Dash, dcc, html, Input, Output
# import requests
# from dash import dash_table
# import plotly.express as px
# import pandas as pd

# # Define the callback for map visualization and the violation table
# def register_callbacks(app):

#     @app.callback(
#         [Output('map-visualization', 'figure'),
#          Output('violation-table', 'data')],
#         [Input('violation-filter', 'value')]
#     )
#     def update_map_and_table(filter_value):
#         # Fetch the violation data from the backend
#         response = requests.get('http://localhost:5000/get_violations')  # Assuming you have this endpoint
#         if response.status_code == 200:
#             violations = response.json()

#             # Filter data based on dropdown
#             df = pd.DataFrame(violations)
#             if filter_value != 'ALL':
#                 df = df[df['violation_type'] == filter_value]

#             # Create map visualization
#             fig = px.scatter_mapbox(
#                 df,
#                 lat='latitude',
#                 lon='longitude',
#                 hover_name='license_plate',
#                 hover_data=['speed', 'timestamp'],
#                 zoom=10,
#                 mapbox_style="open-street-map"
#             )

#             # Return updated map and table data
#             return fig, df.to_dict('records')

#         return {}, []  # Return empty if no data


import requests
import pandas as pd
import plotly.express as px
from dash import Input, Output

def register_callbacks(app):
    @app.callback(
        [Output('map-visualization', 'figure'),
         Output('violation-table', 'data')],
        [Input('violation-filter', 'value')]
    )
    def update_map_and_table(filter_value):
        try:
            # Fetch the violation data from the backend
            response = requests.get('http://localhost:5000/get_violations')
            
            # Check for successful response
            if response.status_code == 200:
                violations = response.json()

                # Convert to DataFrame
                df = pd.DataFrame(violations)
                print(df.head())  # Debug: Print the DataFrame

                # Check if required columns are present
                required_columns = {'latitude', 'longitude', 'license_plate', 'speed', 'timestamp', 'violation_type'}
                missing_columns = required_columns - set(df.columns)
                if missing_columns:
                    print(f"Missing required columns in the data: {missing_columns}")
                    return {}, []  # Return empty map and table if columns are missing

                # Filter data based on dropdown
                if filter_value != 'ALL':
                    df = df[df['violation_type'] == filter_value]

                # Handle empty DataFrame after filtering
                if df.empty:
                    print("No data available after filtering.")
                    return {}, []  # Return empty map and table if no data is available

                # Create map visualization
                fig = px.scatter_mapbox(
                    df,
                    lat='latitude',
                    lon='longitude',
                    hover_name='license_plate',
                    hover_data=['speed', 'timestamp'],
                    zoom=10,
                    mapbox_style="open-street-map"
                )

                # Return updated map and table data
                return fig, df.to_dict('records')

            else:
                print(f"Backend error: {response.status_code} - {response.text}")
                return {}, []  # Return empty map and table in case of backend failure

        except Exception as e:
            print(f"Error in callback: {e}")
            return {}, []  # Return empty map and table in case of exception
