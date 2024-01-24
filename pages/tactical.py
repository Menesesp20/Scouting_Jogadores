import pandas as pd
import numpy as np
import json
import ast

import streamlit as st

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

import datetime

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image
from soccerplots.radar_chart import Radar

from mplsoccer import Pitch, VerticalPitch, PyPizza

import math
import functions

from scipy.stats import stats

import matplotlib as mpl
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# FONT FAMILY
# Set the Lato font file path
lato_path = './Fonts/Lato-Black.ttf'

# Register the Lato font with Matplotlib
custom_font = FontProperties(fname=lato_path)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.header('Game Analysis')

# DICTIONARY OF COLORS

clubColors = {'Brazil' : ['#fadb04', '#1c3474'],
            'Portugal' : ['#e1231b', '#004595'],
            'Argentina' : ['#52a9dc', '#dbe4ea'],
            'Saudi Arabia' : ['#145735', '#dbe4ea'],
            'Ghana' : ['#145735', '#dbe4ea'],
            'Serbia' : ['#FF0000', '#ffffff'],
            'Spain' : ['#FF0000', '#ffffff'],
            'Germany' : ['#aa9e56', '#FF0000'],
            'France' : ['#202960', '#d10827'],
            'Poland' : ['#d10827', '#ffffff'],
            'Morocco' : ['#db221b', '#044c34'],
            'Croatia' : ['#e71c23', '#3f85c5'],
            'Netherlands' : ['#f46c24', '#dcd9d7'],
            'Senegal' : ['#34964a', '#eedf36'],
            'Denmark' : ['#cb1617', '#ffffff'],
            'Iran' : ['#269b44', '#dd1212'],
            'Belgium' : ['#ff0000', '#e30613'],
            'USA' : ['#ff0000', '#202960'],
            'Switzerland' : ['#ff0000', '#ffffff'],
            'Australia' : ['#202960', '#e30613'],
            'Wales' : ['#ff0000', '#ffffff'],
            'Mexico' : ['#00a94f', '#ff0000'],
            'Uruguay' : ['#52a9dc', '#ffffff'],
            'Canada' : ['#ff0000', '#ff0000'],
            'Costa Rica' : ['#ff0000', '#202960'],
            'Catar' : ['#7f1244', '#ffffff'],
            'Ecuador' : ['#ffce00', '#002255'],
            'South Korea' : ['#021858', '#ffffff'],
            'Real Madrid' : ['#064d93', '#E8E8E8'],
            'Liverpool' : ['#FF0000', '#E8E8E8']}

@st.cache_data(ttl=86400)
def load_Opta(filePathOPTA):
    df = pd.read_csv(filePathOPTA)

    df['Match'] = df['home_Team'] + ' vs ' + df['away_Team']

    df['qualifier_id'] = df['qualifiers'].apply(str).apply(lambda x: functions.get_values_by_qualifier(x, 'qualifier_id', [1, 2, 4, 5, 6, 7, 8, 22, 23, 24, 25, 26, 28, 29,
                                                                                                                96, 107, 154, 155, 157, 160, 195, 196, 210, 214, 215,
                                                                                                                218, 223, 224, 225]))

    # List of actions where endX and endY should be equal to x and y
    actions_to_correct = ['MissedShots', 'Save', 'KeeperPickup', 'Goal', 'Claim', 'Tackle', 'BallRecovery', 
                        'Challenge', 'TakeOn', 'BlockedPass', 'Clearance', 'Aerial', 'Interception', 'Foul', 'SavedShot']

    # Correct the dataset using lambda function
    df.loc[df['typedisplayName'].isin(actions_to_correct), 'endX'] = df['x']
    df.loc[df['typedisplayName'].isin(actions_to_correct), 'endY'] = df['y']

    # Assuming df["minute"] and df["second"] are already defined
    df["matchTimestamp"] = 60 * df["minute"] + df["second"]
    # Convert total seconds into minutes and seconds
    df["matchTimestamp"] = df["matchTimestamp"].apply(lambda x: f"{x // 60}:{x % 60:02}")

    #df["matchTimestamp"] = pd.to_datetime(df["matchTimestamp"], unit='s')
    df.drop_duplicates(subset=['name', 'matchTimestamp', 'team', 'typedisplayName', 'x', 'y'], keep='first', inplace=True)

    # Shift the player name and team columns to get the subsequent event's player and team
    df['next_player'] = df['name'].shift(-1)
    df['next_team'] = df['team'].shift(-1)

    # Create the Receiver column
    df['Receiver'] = None
    mask = (df['typedisplayName'] == "Pass") & (df['team'] == df['next_team'])
    df.loc[mask, 'Receiver'] = df['next_player']
    # Remove non-Pass rows from the "Recipient" column
    df.loc[df['typedisplayName'] != 'Pass', 'Receiver'] = ''

    df = functions.xT(df)
    df = functions.xT_Intercepted(df)
    df = functions.metric_1v1(df)

    df = functions.progressive_Pass(df)
    df = functions.create_Carry(df)
    df = functions.create_CarryProg(df)

    ############################################################################################################################################################################################################

    df['Between_Lines'] = df.apply(lambda row: True if row['typedisplayName'] == 'Pass' and 73 <= row['endX'] <= 83 and 21.1 <= row['endY'] <= 78.9 else False, axis=1)

    ############################################################################################################################################################################################################

    df['Pass_1/3'] = df.apply(lambda row: True if row['typedisplayName'] == 'Pass' and row['endX'] > 78 and row['endY'] > 0 else False, axis=1)

    ############################################################################################################################################################################################################

    df['High_Recovery'] = df.apply(lambda row: True if row['typedisplayName'] == 'BallRecovery' and row['x'] >= 65 else False, axis=1)

    ############################################################################################################################################################################################################

    df['Between_Lines_Success'] = df.apply(lambda row: True if row['Between_Lines'] and row['outcomeType.value'] == 1 else False, axis=1)

    ############################################################################################################################################################################################################

    df['Pass_1/3_Success'] = df.apply(lambda row: True if row['Pass_1/3'] and row['outcomeType.value'] == 1 else False, axis=1)

    ############################################################################################################################################################################################################

    df['initialDistancefromgoal'] = df.apply(lambda row: np.sqrt(((100 - row['x'])**2) + ((50 - row['y'])**2)) if row['typedisplayName'] == 'Pass' else False, axis=1)
    df['finalDistancefromgoal'] = df.apply(lambda row: np.sqrt(((100 - row['endX'])**2) + ((50 - row['endY'])**2)) if row['typedisplayName'] == 'Pass' else False, axis=1)

    df['deepCompletion'] = df.apply(lambda row: np.where(((row['finalDistancefromgoal'] <= 20) & (row['initialDistancefromgoal'] >= 20)), True, False) if row['initialDistancefromgoal'] != False and row['initialDistancefromgoal'] != False else False, axis=1)

    ############################################################################################################################################################################################################

    df.sort_values(by=['Match_ID', 'matchTimestamp'], inplace=True, ascending=[True, True])

    #df['Match_ID'] = df['Match_ID'].apply(lambda x: 'Play Off Semi-Final 2nd' if x == 48 else x)

    #df['Match_ID'] = df['Match_ID'].apply(lambda x: 'Play Off Semi-Final 1st' if x == 47 else x)

    df.drop_duplicates(subset=['name', 'matchTimestamp', 'team', 'typedisplayName', 'x', 'y'], keep='first', inplace=True)

    def concatFotMob_WhoScored(df, filePath):
        fotmob = pd.read_csv(filePath)
        fotmob = fotmob.drop_duplicates(subset='id')
        fotmob=fotmob.drop(['eventType','team', 'playerId', 'playerName', 'eventTime', 'eventTimeAdd','isBlocked', 'shotType', 'situation', 'period', 'Match_ID'], axis=1)
        df = df.merge(fotmob, left_on=['id'], right_on=['id'], how='left', suffixes=['x', ''])
        x_columns = [col for col in df.columns if col != 'is_own_goal']
        df = df[x_columns]
        df.rename(columns={'expectedGoal': 'xG'}, inplace=True)
        df.rename(columns={'expectedGOT': 'xGOT'}, inplace=True)
        return df

    #df = concatFotMob_WhoScored(df, '../whoscored_scraper/shots_data_FotMob_Sheffield Wed_Last10Games.csv')

    # Convert string representation to list of dictionaries
    df['qualifiers'] = df['qualifiers'].apply(ast.literal_eval)

    # Extract length values
    df['Length'] = df['qualifiers'].apply(lambda x: [item['value'] for item in x if item['type']['displayName'] == 'Length'][0] if any('GoalKick' in item['type']['displayName'] for item in x) else None)

    # Convert again to string
    df['qualifiers'] = df['qualifiers'].apply(str)

    return df

champions = load_Opta('Data/Opta/Last5Games_Benfica.csv')
champions['League'] = 'Liga Betclic'

with st.form("select-buttons"):
    options_Leagues = st.sidebar.selectbox(
        'Choose League from the club you want analyse:',
        champions.League.unique())

    options_Clubs = st.sidebar.selectbox(
        'Choose Club you want analyse:',
        sorted(champions.loc[champions.League == options_Leagues]['team'].unique()))

    options_MatchDay = st.sidebar.selectbox(
        'Choose MatchDay:',
        sorted(champions['Match_ID'].unique()))

    options_Players = st.sidebar.selectbox(
        'Choose Player you want analyse:',
        sorted(champions.loc[champions.team == options_Clubs]['name'].unique()))

    options_AfterSub = st.sidebar.selectbox(
        'Choose Player you want analyse:',
        ['No', 'Yes'])

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    btn1 = col1.form_submit_button(label='How they come out?')
    btn2 = col2.form_submit_button(label='How they build up?')
    btn3 = col3.form_submit_button(label='Where they create chances & score?')
    btn4 = col4.form_submit_button(label='They press high?')
    btn5 = col5.form_submit_button(label='Do we control the game?')
    btn6 = col6.form_submit_button(label='Team Pass Network')
    btn7 = col7.form_submit_button(label='Player Pass Network')

#col1, col2, col3, col4, col5, col6 = st.columns(6)
goalKick_DF = champions.copy()

if btn1:
        goalKick_DF['Length'].fillna(0, inplace=True)

        goalKick_DF['Length'] = goalKick_DF['Length'].astype(float)

        goalKick_DF["matchTimestamp"] = 60 * goalKick_DF["minute"] + goalKick_DF["second"]
        goalKick_DF["matchTimestamp"] = pd.to_datetime(goalKick_DF["matchTimestamp"], unit='s')

        st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
        figGkick = functions.GoalKick(goalKick_DF, options_Clubs, 3, 100)
        st.pyplot(figGkick)

if btn2:
        goalKick_DF['Length'].fillna(0, inplace=True)

        goalKick_DF['Length'] = goalKick_DF['Length'].astype(float)

        goalKick_DF["matchTimestamp"] = 60 * goalKick_DF["minute"] + goalKick_DF["second"]
        goalKick_DF["matchTimestamp"] = pd.to_datetime(goalKick_DF["matchTimestamp"], unit='s')

        st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
        figBuildUp = functions.draw_heatmap_construcao(goalKick_DF, options_Clubs, 5, 250)
        st.pyplot(figBuildUp)

if btn3:
    st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
    figChances = functions.finalThird(champions, options_Clubs, 4)
    st.pyplot(figChances)

if btn4:
    st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
    figPress = functions.highTurnovers(champions, options_Clubs)
    st.pyplot(figPress)

if btn5:
    st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
    fig_xTFlow = functions.xT_Flow(champions, options_Leagues, options_Clubs, options_MatchDay)
    st.pyplot(fig_xTFlow)

if btn6:
    st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
    fig_TeamNetwork = functions.passing_networkWhoScored(champions, options_Clubs, options_MatchDay)
    st.pyplot(fig_TeamNetwork)

if btn7:
    st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
    fig_PlayerNetwork = functions.player_Network(champions, options_Players, options_Clubs, options_MatchDay)
    st.pyplot(fig_PlayerNetwork)
