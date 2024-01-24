import streamlit as st
import pandas as pd

# Load your data into a DataFrame called df
@st.cache_data(ttl=86400)
def load_data(filePath):
    return pd.read_csv(filePath)

df = load_data('./Data/data.csv')
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df['Age']  = df['Age'].astype(int)

# Begin the layout
st.sidebar.title('Player Selection')
# Assuming 'Player Name' is a column in your dataframe
player_name = st.sidebar.selectbox('Select the Player', df['Player'].unique())

# Display player's basic info - Adjust according to your DataFrame's structure
player_info = df[df['Player'] == player_name]
st.sidebar.table(player_info[['Age', 'Team', 'Height', 'Foot']])

st.title('Player Performance Dashboard')

# Metrics and stats in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.header('ID Card')
    # Assuming you have a function to display the player's ID card details
    st.write('Details to be displayed here')

with col2:
    st.header('Minutes')
    # Example of a progress bar
    minutes_played = 90  # Dummy data, replace with actual
    st.progress(minutes_played / 90)

with col3:
    st.header('Appearances')
    # Displaying some stats
    st.metric(label='Goals', value='0')  # Replace with actual data
    st.metric(label='Assists', value='1')  # Replace with actual data

# More detailed metrics - you would replace the placeholder text with actual metrics
st.header('Detailed Metrics')
metric1, metric2, metric3 = st.columns(3)
with metric1:
    st.subheader('Passing')
    st.write('Pass Success: ...')
    st.write('Key Passes: ...')

with metric2:
    st.subheader('Defending')
    st.write('Tackles Won: ...')
    st.write('Interceptions: ...')

with metric3:
    st.subheader('Physical')
    st.write('Sprints: ...')
    st.write('Distance Covered: ...')

# Trendlines and historical data in tabs
tab1, tab2 = st.tabs(['Ability Trendline', 'History'])
with tab1:
    st.write('Graph for Ability over Time here')

with tab2:
    st.write('Table or Graph for Historical Data here')

# Footer - place for additional notes or actions
st.write('Notes or additional actions here')