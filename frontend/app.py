# """This script initializes a Dash application by importing and setting a layout from the layout module. It then registers the necessary callbacks for the app using the register_callbacks function from the callbacks module. Finally, it runs the app in debug mode, allowing for live updates and error tracking during development."""

# # frontend/app.py
# from dash import Dash
# from layout import layout
# from callbacks import register_callbacks

# # Initialize Dash app
# app = Dash(__name__)
# app.layout = layout

# # Register callbacks
# register_callbacks(app)

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)




# # # frontend/app.py

# import sys
# print(sys.executable)
# from dash import Dash
# from dash import dash_bootstrap_components as dbc
# from layout import layout
# from callbacks import register_callbacks

# # Initialize Dash app with Bootstrap theme
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = layout

# # Register callbacks
# register_callbacks(app)

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)


import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import cv2
import threading
import time
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Shared DataFrame for real-time updates
global_df = pd.DataFrame(columns=["License Plate", "Speed", "Latitude", "Longitude", "Timestamp", "Violation"])

# App Layout
app.layout = html.Div([
    html.H1("Vehicle Violation Dashboard", style={"text-align": "center"}),
    dcc.Dropdown(
        id="violation_filter",
        options=[
            {"label": "All Violations", "value": "All"},
            {"label": "Speeding", "value": "Speeding"},
            {"label": "None", "value": "None"}
        ],
        value="All",  # Default value
        style={"width": "50%"}
    ),
    dcc.Graph(id="violation_graph"),
    html.Table([
        html.Thead(html.Tr([html.Th(col) for col in global_df.columns])),
        html.Tbody(id="data_table")
    ])
])

# Video Processing Function
def process_video(video_source='s1900-151662242.mp4'):
    global global_df
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to grab frame.")
            break

        # Example: Dummy Processing Logic
        # Replace this with your actual detection logic (e.g., license plate recognition, speed detection)
        license_plate = "ABC123"
        speed = 80  # Example speed
        latitude, longitude = 40.7128, -74.0060  # Example GPS location
        violation = "Speeding" if speed > 70 else "None"

        # Add data to the global dataframe
        new_data = {
            "License Plate": license_plate,
            "Speed": speed,
            "Latitude": latitude,
            "Longitude": longitude,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Violation": violation
        }
        global_df = pd.concat([global_df, pd.DataFrame([new_data])], ignore_index=True)

        # Limit the DataFrame size to avoid memory issues
        if len(global_df) > 1000:
            global_df = global_df.tail(1000)

        # Simulate processing delay (adjust based on your actual processing logic)
        time.sleep(0.1)

    cap.release()

# Callback to update dashboard
@app.callback(
    [Output("violation_graph", "figure"),
     Output("data_table", "children")],
    [Input("violation_filter", "value")]
)
def update_dashboard(selected_violation):
    global global_df

    # Filter data based on violation type
    if selected_violation == "All":
        filtered_df = global_df
    else:
        filtered_df = global_df[global_df["Violation"] == selected_violation]

    # If no data, show empty graph and message
    if filtered_df.empty:
        fig = px.scatter(title="No Data Available")
        table_rows = [html.Tr([html.Td("No data available")])]
        return fig, table_rows

    # Plot the data on a scatter plot
    fig = px.scatter(
        filtered_df,
        x="Longitude",
        y="Latitude",
        color="Violation",
        size="Speed",
        hover_data=["License Plate", "Timestamp"],
        title="Vehicle Violations"
    )

    # Create rows for the table
    table_rows = [
        html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns])
        for i in range(len(filtered_df))
    ]

    return fig, table_rows

# Run video processing in a separate thread
video_path = "path_to_your_video.mp4"  # Replace with the path to your video file
video_thread = threading.Thread(target=process_video, args=(video_path,))
video_thread.daemon = True
video_thread.start()

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)




    
    
