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
    wyscout.drop(['Unnamed: 0'], axis=1, inplace=True)
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

def get_TeamSimilarity(df, teamName, NumTeam):

    # List of specified attributes
    specified_attributes = ['Pass Ability', 'KeyPass Ability', 'SetPieces Ability', 'Dribbling Ability', 'Create Chances Ability',
                            'Sight play', 'Concentration Ability', 'Finishing Ability', 'Heading Ability', 'Interception Ability',
                            'Tackle Ability', 'Aerial Ability', 'Defensive Ability', 'crossing', 'defending1v1', 
                            'decisionMake', 'touchQuality']

    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Now, adjusted_attributes will contain only non-numeric columns from the original specified_attributes list.

    X = df[numeric_cols].values
    y = df['Team'].values

    # Standardize the data
    X_std = StandardScaler().fit_transform(X)

    # Apply PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_std)

    # Plot cumulative explained variance to determine the number of components
    cumulative_explained_variance = np.cumsum(pca.explained_variance_ratio_)

    # Based on the plot, we'll choose the number of components where cumulative explained variance is above 95%
    n_components = np.argmax(cumulative_explained_variance > 0.95) + 1

    # Transform the data using the selected number of PCA components
    X_pca_reduced = X_pca[:, :n_components]

    # Create a DataFrame for the PCA transformed data
    columns = ["PCA" + str(i+1) for i in range(n_components)]
    pca_df = pd.DataFrame(X_pca_reduced, columns=columns, index=y)

    # Compute the correlation matrix
    corr_matrix = pca_df.T.corr(method='pearson')

    def GetSimilarPlayers(teamName, NumTeam, corr_matrix):
        """Retrieve the top 'numPlayers' similar players to the given 'PlayerName' based on the correlation matrix."""
        
        # Create a DataFrame to store the results
        SimPlayers = pd.DataFrame(columns=['Team', 'Similar Team', 'Correlation Factor'])

        # Extract the correlation values for the specified player
        correlations = corr_matrix[teamName]
        
        # Drop the player itself from the list
        correlations = correlations.drop(teamName)
        
        i = 0
        for i in range(0, NumTeam):
            row = corr_matrix.loc[corr_matrix.index == teamName].squeeze()

            SimPlayers.at[i, 'Team'] = teamName
            SimPlayers.at[i, 'Similar Team'] = row.nlargest(i+2).sort_values(ascending=True).index[0]
            SimPlayers.at[i, 'Correlation Factor'] = round(row.nlargest(i+2).sort_values(ascending=True)[0], 2)

            i = i+1

        return SimPlayers

    df_correlatedPlayers = GetSimilarPlayers(teamName, NumTeam, corr_matrix)

    df_correlatedPlayers = df_correlatedPlayers.sort_values(by='Correlation Factor', ascending=False).reset_index(drop=True)

    return df_correlatedPlayers

# List of columns to sum
sum_columns = ['Pass Ability', 'KeyPass Ability', 'SetPieces Ability', 'Dribbling Ability', 'Create Chances Ability',
                'Sight play', 'Concentration Ability', 'Finishing Ability', 'Heading Ability', 'Interception Ability',
                'Tackle Ability', 'Aerial Ability', 'Defensive Ability', 'crossing', 'defending1v1', 'positioning Defence', 
                'positioning Midfield', 'ballPlaying Deep', 'progressiveRuns',
                'runs', 'decisionMake', 'touchQuality']

# Group the dataframe by 'teamId' and sum the specified columns
summed_df = wyscout.groupby('Team')[sum_columns].sum().reset_index()

# Count the number of players per team
player_count = wyscout.groupby('Team')['Player'].count().reset_index()
player_count.rename(columns={'Players': 'Player Count'}, inplace=True)

# Merge the summed columns and player count dataframes
grouped_df = pd.merge(summed_df, player_count, on='Team')

grouped_df = grouped_df[grouped_df['Team'] != '0'].reset_index(drop=True)

grouped_df = grouped_df.sort_values('Player', ascending=False).reset_index(drop=True)

# Calculate the average ability for each team by dividing the summed abilities by the number of players
for col in sum_columns:
    grouped_df[col] = round(grouped_df[col] / grouped_df['Player'], 2)

grouped_df.head()

with st.form("select-buttons-similar"):
    options_Similar = st.sidebar.selectbox('What to get similar teams?', ['Yes', 'No'])

    if options_Similar == 'Yes':
        options_Team = st.sidebar.selectbox('Choose Team', wyscout.Team.unique())

        btn1 = st.form_submit_button(label='Similar Teams')

if btn1:

        similar_Teams = get_TeamSimilarity(grouped_df, options_Team, 10)

        st.dataframe(similar_Teams, height=500, use_container_width=True)