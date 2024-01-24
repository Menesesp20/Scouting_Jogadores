import pandas as pd
import streamlit as st

import numpy as np

import matplotlib.pyplot as plt
import datetime

from matplotlib import font_manager

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from PIL import Image
import base64

font_path = './Fonts/Lato-Black.ttf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

# Courier New
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title="Recruitment App",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded")

st.title('Data Hub')

st.markdown("""
This app performs visualization from sports data to improve the club decision make!
* **Data source:** WyScout & OPTA.

* Choose one tier, one league, one role and choose the Under age you want to get all the best players in each role

* **Tier 0 - Best 5 leagues.**
* **Tier 1 - Best european leagues outside Big5 and best south american.**
* **Tier 2 - 2 Divisions from the BIG5 and second tier european leagues plus best asian leagues.**
* **Tier 3 - 3 Divisions from the BIG5 and third tier european leagues plus second tier american leagues.**
* **Tier 4 - Exotic Markets like Estonia, Luxembourg, etc.**
""")

st.sidebar.header('Scouting Hub')

@st.cache_data(ttl=86400)
def load_data(filePath):
    wyscout = pd.read_parquet(filePath)
    #wyscout.drop(['Unnamed: 0'], axis=1, inplace=True)
    wyscout['Age']  = wyscout['Age'].astype(int)
    
    return wyscout

wyscout = load_data('./Data/data.parquet')

options_Tiers = st.sidebar.multiselect(
    'Choose the tiers you want',
    wyscout.Tier.unique(), wyscout.Tier.unique()[0])

# Common filtering criteria
common_filterLeagues = (wyscout['Tier'].isin(options_Tiers))

if len(common_filterLeagues) == 0:
    # Add only the common filtering criteria when options_Leagues is empty
    leagues = wyscout.Comp.unique()
else:
    # Add the common filtering criteria and the league filter when options_Leagues is not empty
    leagues = wyscout.loc[common_filterLeagues].Comp.unique()

options_Leagues = st.sidebar.multiselect(
    'Choose the leagues you want',
    leagues, leagues[0])

options_Roles = st.sidebar.multiselect(
    'Choose the roles you want',
    wyscout.Role.unique(), wyscout.Role.unique()[0])

options_UnderAge = st.sidebar.selectbox(
    'Choose Age (Under)',
    sorted(wyscout.Age.unique(), reverse = True))

# Common filtering criteria
common_filter = (wyscout['Tier'].isin(options_Tiers)) & \
                (wyscout['Age'] <= options_UnderAge) & \
                ((wyscout['Role'].isin(options_Roles)) | (wyscout['Role2'].isin(options_Roles))) 

if len(options_Leagues) == 0:
    # Add only the common filtering criteria when options_Leagues is empty
    data = wyscout.loc[common_filter][['Player', 'Age', 'Market value', 'Contract expires', 'Team', 'Comp', 'Tier', 'Role', 'Role2', 'Score', 'Potential']].sort_values('Score', ascending=False).reset_index(drop=True)
else:
    # Add the common filtering criteria and the league filter when options_Leagues is not empty
    data = wyscout.loc[common_filter & (wyscout['Comp'].isin(options_Leagues))][['Player', 'Age', 'Market value', 'Contract expires', 'Team', 'Comp', 'Tier', 'Role', 'Role2', 'Score', 'Potential']].sort_values('Score', ascending=False).reset_index(drop=True)

st.dataframe(data, height=500, use_container_width=True)