import streamlit as st
import pandas as pd
import os

from datetime import datetime
import gps_functions

st.sidebar.header('GPS Center')

# Assuming you want to use the times from specific dates as default values
def validate_datetime(datetime_str):
    try:
        return datetime.strptime(datetime_str, '%d-%m-%Y %H:%M:%S'), None
    except ValueError:
        return None, "Invalid datetime format, please use DD-MM-YYYY HH:MM:SS"

# Default datetime in YYYY-MM-DD HH:MM:SS format
default_start_datetime = '12-11-2023 15:45:11'
default_end_datetime = '12-11-2023 16:33:00'

col1, col2 = st.columns(2)

with col1:
    # User inputs for datetime
    game_start_str = st.text_input('Game start (DD-MM-YYYY HH:MM:SS):', default_start_datetime)

with col2:
    game_end_str = st.text_input('Game end (DD-MM-YYYY HH:MM:SS):', default_end_datetime)

# Validation and conversion to datetime objects
game_start_input, error_start = validate_datetime(game_start_str)
game_end_input, error_end = validate_datetime(game_end_str)

if error_start:
    st.sidebar.error(error_start)

if error_end:
    st.sidebar.error(error_end)

game_start_pd = pd.to_datetime(game_start_str)
game_end_pd = pd.to_datetime(game_end_str)

# Function to get a tuple of floats from a string
def get_coords(input_str):
    try:
        coords = tuple(map(float, input_str.split(',')))
        if len(coords) == 2:
            return coords, None
        else:
            return None, "Please enter coordinates in the format: lat,lon"
    except ValueError:
        return None, "Invalid input. Ensure you are entering numbers."

# Predefined values for each point
default_values = {
    'A': '-3.745538,-38.537282',
    'B': '-3.746449,-38.537013',
    'C': '-3.746257,-38.536377',
    'D': '-3.745350,-38.536645'
}

reference_points = {}
errors = {}

# Creating two columns for input fields
col1, col2 = st.columns(2)

with col1:
    for point in ['A', 'B']:
        user_input = st.text_input(f'Coordinates for point {point} (format: lat,lon)', default_values[point])
        coords, error = get_coords(user_input)
        if coords:
            reference_points[point] = coords
        if error:
            errors[point] = error

with col2:
    for point in ['C', 'D']:
        user_input = st.text_input(f'Coordinates for point {point} (format: lat,lon)', default_values[point])
        coords, error = get_coords(user_input)
        if coords:
            reference_points[point] = coords
        if error:
            errors[point] = error

# Display errors if any
for point, error in errors.items():
    st.error(f'Error for point {point}: {error}')

# Creating two columns for input fields
col1, col2 = st.columns(2)

with col1:
    pitch_length = int(st.text_input('Pitch Length', 105))

with col2:
    pitch_width = int(st.text_input('Pitch Width', 65))

cutoff_frequency = float(st.sidebar.text_input('Cutoff Frequency', 2.0))
sampling_frequency = int(st.sidebar.text_input('Sampling Frequency', 10))
order = int(st.sidebar.text_input('Order', 3))

choose_Viz = st.sidebar.selectbox('Visualization:', ['Sprints', 'Heat Map'])

sprints_Map_Choose = st.sidebar.selectbox('Sprints Map: (Choose Team or Player)', ['Team', 'Player'])

@st.cache_data(ttl=86400)
def get_GPS_Sprint_Data(game_start, game_end, cutoff_frequency, sampling_frequency, order):
    # Define the path and load CSV files
    path = 'Data/GPS/12.11.2023 - CSC x Mirassol'
    files = [f for f in os.listdir(path) if f.endswith('.csv')]

    # Efficiently extract player names
    player_names = [file.split("for ")[1].split(".")[0] for file in files]

    # Filter files based on player names
    filtered_files = [file for file in files if any(player in file for player in player_names)]

    # Initialize a list to store DataFrames
    lista_df = []

    # Process each file
    for file in filtered_files:
        # Load data
        data = pd.read_csv(os.path.join(path, file), skiprows=8, delimiter=";", decimal=",")

        data['playerName'] = file.split("for ")[1].split(".")[0]

        # Process X and Y coordinates
        data['Y'], data['X'] = zip(*data.apply(lambda row: gps_functions.convert_to_cartesian(row['Latitude'], row['Longitude']), axis=1))

        data['Timestamp'] = pd.to_datetime(data['Timestamp'])

        # Apply lowpass filter
        data['X_filtered'] = gps_functions.butter_lowpass_filter(data['X'], cutoff_frequency, sampling_frequency, order)
        data['Y_filtered'] = gps_functions.butter_lowpass_filter(data['Y'], cutoff_frequency, sampling_frequency, order)
        
        # Append processed DataFrame to the list
        lista_df.append(data)

    # Concatenate all DataFrames outside the loop
    df = pd.concat(lista_df, axis=0)

    # Filter data for a specific time interval
    half_data = df[(df['Timestamp'] >= game_start) & (df['Timestamp'] <= game_end)]

    # Filter for sprints
    half_data_Sprints = half_data[(half_data['Velocity'] >= 30)].reset_index(drop=True)
    half_data_Sprints['endX'] = half_data_Sprints['X_filtered'].shift()
    half_data_Sprints['endY'] = half_data_Sprints['Y_filtered'].shift()

    return half_data_Sprints

@st.cache_data(ttl=86400)
def get_GPS_Data(game_start, game_end, cutoff_frequency, sampling_frequency, order):
    # Define the path and load CSV files
    path = 'Data/GPS/12.11.2023 - CSC x Mirassol'
    files = [f for f in os.listdir(path) if f.endswith('.csv')]

    # Efficiently extract player names
    player_names = [file.split("for ")[1].split(".")[0] for file in files]

    # Filter files based on player names
    filtered_files = [file for file in files if any(player in file for player in player_names)]

    # Initialize a list to store DataFrames
    lista_df = []

    # Process each file
    for file in filtered_files:
        # Load data
        data = pd.read_csv(os.path.join(path, file), skiprows=8, delimiter=";", decimal=",")

        data['playerName'] = file.split("for ")[1].split(".")[0]

        # Process X and Y coordinates
        data['Y'], data['X'] = zip(*data.apply(lambda row: gps_functions.convert_to_cartesian(row['Latitude'], row['Longitude']), axis=1))

        data['Timestamp'] = pd.to_datetime(data['Timestamp'])

        # Apply lowpass filter
        data['X_filtered'] = gps_functions.butter_lowpass_filter(data['X'], cutoff_frequency, sampling_frequency, order)
        data['Y_filtered'] = gps_functions.butter_lowpass_filter(data['Y'], cutoff_frequency, sampling_frequency, order)
        
        # Append processed DataFrame to the list
        lista_df.append(data)

    # Concatenate all DataFrames outside the loop
    df = pd.concat(lista_df, axis=0)

    # Filter data for a specific time interval
    half_data = df[(df['Timestamp'] >= game_start) & (df['Timestamp'] <= game_end)]
    half_data = half_data[(half_data['Velocity'] >= 5)]

    return half_data

if (choose_Viz == 'Heat Map'):
    gps_Data = get_GPS_Data(game_start_pd, game_end_pd, cutoff_frequency, sampling_frequency, order)

elif (choose_Viz == 'Sprints'):
    gps_SprintData = get_GPS_Sprint_Data(game_start_pd, game_end_pd, cutoff_frequency, sampling_frequency, order)

if (sprints_Map_Choose == 'Team') & (choose_Viz == 'Sprints'):
    sprints_Team = gps_functions.sprints_Map_Team(gps_SprintData, pitch_length, pitch_width)
    st.pyplot(sprints_Team)

elif (sprints_Map_Choose == 'Player') & (choose_Viz == 'Sprints'):
    sprints_by_Player = gps_functions.sprints_Map_Player(gps_SprintData, pitch_length, pitch_width)
    st.pyplot(sprints_by_Player)

if (sprints_Map_Choose == 'Team') & (choose_Viz == 'Heat Map'):
    heatMap_Team = gps_functions.heatMap_GPS_Team(gps_Data, pitch_length, pitch_width)
    st.pyplot(heatMap_Team)

elif (sprints_Map_Choose == 'Player') & (choose_Viz == 'Heat Map'):
    heatMap_by_Player = gps_functions.heatMap_GPS_Player(gps_Data, pitch_length, pitch_width)
    st.pyplot(heatMap_by_Player)