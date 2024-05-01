import pandas as pd
import numpy as np
import streamlit as st

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties

import datetime

from highlight_text import  ax_text, fig_text

from soccerplots.utils import add_image
from soccerplots.radar_chart import Radar

from mplsoccer import Pitch, VerticalPitch, PyPizza

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Image, PageBreak, Spacer, Frame, PageTemplate
from reportlab.lib.units import inch
from PIL import Image as PILImage
import io

import math

from scipy.stats import stats

import matplotlib.pyplot as plt

import re

import os
import warnings
warnings.filterwarnings("ignore")

# FONT FAMILY
# Set the Lato font file path
lato_path = 'Fonts/Lato-Black.ttf'

# Visualization Section of the Web App starts here

# Register the Lato font with Matplotlib
custom_font = FontProperties(fname=lato_path)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.header('Player Recruitment')

@st.cache_data(ttl=86400)
def load_data(filePath):
    data = pd.read_parquet(filePath)
    return data

data = load_data('./Data/data.parquet')

@st.cache_data(ttl=86400)
def load_wyscout(filePath):
    wyscout = pd.read_parquet(filePath)
    return wyscout

wyscout = load_wyscout('./Data/wyscout.parquet')

#st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
#def loadS3_Data(fileName):
#    s3 = boto3.resource('s3')
#    S3_BUCKET_NAME = 'gpsdataceara'
#    folder_name = 'python/gps/'
#    file_name = fileName
#    key_name = f'{folder_name}{file_name}'

#    s3_object = s3.Object(S3_BUCKET_NAME, key_name)
#    body = s3_object.get()['Body']
#    wyscout = pd.read_csv(body)
#    return wyscout

#wyscout = loadS3_Data('wyscout.csv')

#st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
#def load_dataOPTA(filePath):
#    return pd.read_parquet(filePath)
#opta = load_dataOPTA('./Data/opta.parquet')

center_Back = ['Offensive duels %', 'Prog. runs/90',
               'Passes %', 'Forward passes %', 'Forward passes/90', 'Progressive p./90',
               'PAdj Interceptions', 'PAdj tackles', 'Defensive duels/90', 'Def. duels %',
               'Aerial duels/90', 'Aerial duels %', 'Shots blocked/90']

full_Back = ['Touches box/90', 'Prog. runs/90', 'Deep completions/90', 'Deep crosses/90',
             'Passes %', 'Progressive p./90', 'Key passes/90', 'Crosses/90', 'Third assists/90',
             'Aerial duels %', 'PAdj Interceptions', 'Aerial duels/90', 'Offensive duels %',]

defensive_Midfield  = ['xG/90', 'Shots', 'Prog. runs/90', 'Passes %',
                       'Forward passes %', 'Forward passes/90', 'Progressive p./90',
                       'Aerial duels/90', 'Aerial duels %','PAdj tackles',
                       'PAdj Interceptions', 'Def. duels %', 'Offensive duels %']

Midfield  = ['xG/90', 'Shots', 'Prog. runs/90', 'Progressive p./90',
             'Passes %', 'Forward passes %', 'Forward passes/90', 'xA',
             'Key passes/90', 'Second assists/90', 'Assists', 'Aerial duels %',
             'PAdj Interceptions', 'Def. duels %']

offensive_Midfield = ['Deep completions/90', 'Goals/90', 'Prog. runs/90', 'Progressive p./90',
                      'xA/90', 'xG/90', 'P. penalty area/90',
                      'Touches box/90', 'Key passes/90', 'Passes final 1/3 %',
                      'P. penalty area %', 'Aerial duels %',
                      'Def. actions/90', 'PAdj Interceptions', 'Def. duels %']

offensive_Midfield_BS = ['Aerial duels %', 'xA/90', 'Deep completions/90', 'P. penalty area/90',
                      'Key passes/90', 'Passes final 1/3 %']

Winger = ['Goals', 'xG/90',
          'xA/90', 'Touches box/90', 'Dribbles/90', 'P. penalty area/90', 'Key passes/90',
          'Prog. runs/90', 'Crosses/90', 'Deep crosses/90',
          'Aerial duels %', 'Offensive duels/90', 'PAdj Interceptions']

Forward = ['Goals', 'xG/90', 'Shots target %', 'Goal conversion, %',
           'xA/90', 'Touches box/90', 'Dribbles/90',
           'Aerial duels %', 'Offensive duels/90', 'PAdj Interceptions', 'Aerial duels/90',]

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def bars(data, playerName, club, league, league_Compare, metrics, season, season_Compare, number, minutes, minutes_2, ax):

    if type(season_Compare) != 'str':
            str(season_Compare)
    else:
        pass

    Creation = ['Visão de Jogo', 'Habilidade Criar Chances', 'Habilidade Passe Decisivo', 'Tomada de decisão']

    WithOut_Ball = ['Concentração', 'Habilidade Aérea', 'Habilidade Interceptação', 'Habilidade Desarme', 'Posicionamento Defensivo']

    finalThird = ['Habilidade Drible', 'Habilidade Finalização', 'Tomada de decisão', 'Habilidade Cabeceio']

    buildUp = ['Construção de jogo', 'Habilidade Passe', 'Visão de Jogo', 'Corrida Progressiva']

    setPieces = ['Habilidade Bola Parada']

    playerDF = data.loc[(data['Player'] == playerName) & (data['Team'] == club) & (data['Comp'] == league) & (data['Season'] == season)].reset_index(drop=True)
    position = playerDF['Main Pos'].unique()[0]

    df = data.loc[(data['Season'] == season_Compare) & ((data['League'] == league_Compare) | (data['Player'] == playerName)) &
                  ((data['Minutes played'] >= minutes) | (data['Minutes played'] <= minutes_2)) & (data['Main Pos'] == position)].reset_index(drop=True)
    #fig.set_facecolor('#181818')
    #ax.set_facecolor('#181818')

    # Data
    x = metrics
    max_values = [100] * len(metrics)

    # Iterate through the metrics
    for metric in metrics:
        # Find the maximum value of the current metric
        max_value = df[metric].max()
        # Append the maximum value to the list
        max_values.append(max_value)
        
    current_value = []
    
    player = playerDF.loc[(playerDF['Player'] == playerName) & (playerDF['Team'] == club) & (playerDF['Comp'] == league) & (playerDF['Season'] == season)][metrics].reset_index(drop=True)
    player = list(player.loc[0])
    player = [value * number for value in player]
    
    # Set the maximum limit of each bar using the max_values list
    for i in range(len(metrics)):
        ax.barh(x[i], max_values[i], color='#e9eaea')
        current_value.append(player[i])
        ax.barh(x[i], current_value[i], color='#181818')
        ax.text(current_value[i] + 2, x[i], str(int(current_value[i])), ha='left', va='center', fontsize=17, color='#E8E8E8')

    # Add labels and title
    if metrics == Creation:
        ax_text(x=50, y=4, s='Criação', va='center', ha='center',
                size=25, color='#181818', ax=ax)
        
    elif metrics == WithOut_Ball:
        ax_text(x=50, y=5, s='Sem Bola', va='center', ha='center',
                size=25, color='#181818', ax=ax)
   
    elif metrics == finalThird:
        ax_text(x=50, y=4, s='Meio Campo Ofensivo', va='center', ha='center',
                size=25, color='#181818', ax=ax)
   
    elif metrics == buildUp:
        ax_text(x=50, y=4, s='Construção', va='center', ha='center',
                size=25, color='#181818', ax=ax)

    elif metrics == setPieces:
        ax_text(x=50, y=4, s='Bola Parada', va='center', ha='center',
                size=25, color='#181818', ax=ax)

    ax.tick_params(axis='both', colors='#181818')
    for tick in ax.get_xticklabels():
        tick.set_color('#181818')
    for tick in ax.get_yticklabels():
        tick.set_color('#181818')

    ax.spines['bottom'].set_color('#181818')
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color('#181818')
    ax.spines['right'].set_visible(False)
 
    # Show chart 
    #return plt.show()

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def barsAbility(df, playerName, team, season, league, league_Compare, season_Compare, number, minutes, minutes_2):

    Creation = ['Visão de Jogo', 'Habilidade Criar Chances', 'Habilidade Passe Decisivo', 'Tomada de decisão']

    WithOut_Ball = ['Concentração', 'Habilidade Aérea', 'Habilidade Interceptação', 'Habilidade Desarme', 'Posicionamento Defensivo']

    finalThird = ['Habilidade Drible', 'Habilidade Finalização', 'Tomada de decisão', 'Habilidade Cabeceio']

    buildUp = ['Construção de jogo', 'Habilidade Passe', 'Visão de Jogo', 'Corrida Progressiva']

    setPieces = ['Habilidade Bola Parada']

    metrics_list = [Creation, WithOut_Ball, finalThird, buildUp]

    dataDash = df.loc[(df['Player'] == playerName) & (df['Team'] == team) & (df['Comp'] == league) & (df['Season'] == season)].reset_index(drop=True)
    
    #club = dataDash.Team.unique()
    #club = club[0]
    
    fig, axs = plt.subplots(2, 2, figsize=(20, 12))
    fig.subplots_adjust(hspace=0.3, wspace=0.8)
    fig.set_facecolor('#e9eaea')
    axs = axs.ravel()

    for i, metrics in enumerate(metrics_list):
        ax = axs[i]
        ax.set_facecolor('#e9eaea')
        bars(df, playerName, team, league, league_Compare, metrics, season, season_Compare, number, minutes, minutes_2, ax)

    #fig = add_image(image='../Images/Players/' + league + '/' + club + '/' + playerName + '.png', fig=fig, left=-0.001, bottom=0.85, width=0.08, height=0.23)

    #fig = add_image(image='C:/Users/menes/Documents/Data Hub/Images/Country/' + country + '.png', fig=fig, left=0.08, bottom=0.775, width=0.1, height=0.07)

    # Ensure the 'Images' folder exists
    if not os.path.exists(f'Images/Recruitment/{playerName}'):
        os.makedirs(f'Images/Recruitment/{playerName}')

    # Save the figure
    plt.savefig(f'Images/Recruitment/{playerName}/{playerName} Percentile.png')

    return plt.show()

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def Scatters(data, playerName, team, mode=None):
    
    colorScatter = '#3D3D3D'
    if mode == None:
        color = '#E8E8E8'
        background = '#181818'
    elif mode != None:
        color = '#181818'
        background = '#E8E8E8'
        
    player = data.loc[(data.Player == playerName) & (df['Team'] == team)].reset_index(drop=True)
    position = player['Main Pos'].unique()[0]

    df = data.loc[(data.Tier >= 1) & (data['Minutes played'] >= 2000) & (data['Main Pos'] == position)].reset_index(drop=True)

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(25, 15), dpi=500, facecolor = background)

    ##############################################################################################
    ax[0, 0].set_facecolor(background)
    ax[0, 0].scatter(x=df['Sight play'], y=df['Create Chances Ability'], alpha=.1, lw=1, color='#E8E8E8', hatch='///////')
    ax[0, 0].set_title('Sight play vs Chances', color=color, size=18)
    ax[0, 0].axvline(df['Sight play'].mean(), c=color)
    ax[0, 0].axhline(df['Create Chances Ability'].mean(), c=color)

    ax[0, 0].tick_params(axis='x', colors=color, labelsize=12)
    ax[0, 0].tick_params(axis='y', colors=color, labelsize=12)

    ax[0, 0].spines['bottom'].set_color(color)
    ax[0, 0].spines['top'].set_visible(False)
    ax[0, 0].spines['left'].set_color(color)
    ax[0, 0].spines['right'].set_visible(False)

    for i in range(len(player)):
        ax[0, 0].scatter(x=player['Sight play'].values[i], y=player['Create Chances Ability'].values[i], s=400, c='#FCAC14', lw=3, edgecolor=background, label=playerName, zorder=3)

    ##############################################################################################

    ax[0, 1].set_facecolor(background)
    ax[0, 1].scatter(x=df['KeyPass Ability'], y=df['decisionMake'], alpha=.1, lw=1, color='#E8E8E8', hatch='///////')
    ax[0, 1].set_title('KeyPass vs Decision Make', color=color, size=18)
    ax[0, 1].axvline(df['KeyPass Ability'].mean(), c=color)
    ax[0, 1].axhline(df['decisionMake'].mean(), c=color)

    ax[0, 1].tick_params(axis='x', colors=color, labelsize=12)
    ax[0, 1].tick_params(axis='y', colors=color, labelsize=12)

    ax[0, 1].spines['bottom'].set_color(color)
    ax[0, 1].spines['top'].set_visible(False)
    ax[0, 1].spines['left'].set_color(color)
    ax[0, 1].spines['right'].set_visible(False)

    for i in range(len(player)):
        ax[0, 1].scatter(x=player['KeyPass Ability'].values[i], y=player['decisionMake'].values[i], s=400, c='#FCAC14', lw=2, edgecolor=background, label=playerName, zorder=3)

    ##############################################################################################

    ax[1, 0].set_facecolor(background)
    ax[1, 0].scatter(x=df['Dribbling Ability'], y=df['decisionMake'], alpha=.1, lw=1, color='#E8E8E8', hatch='///////')
    ax[1, 0].set_title('Dribbles vs Decision', color=color, size=18)
    ax[1, 0].axvline(df['Dribbling Ability'].mean(), c=color)
    ax[1, 0].axhline(df['decisionMake'].mean(), c=color)

    ax[1, 0].tick_params(axis='x', colors=color, labelsize=12)
    ax[1, 0].tick_params(axis='y', colors=color, labelsize=12)

    ax[1, 0].spines['bottom'].set_color(color)
    ax[1, 0].spines['top'].set_visible(False)
    ax[1, 0].spines['left'].set_color(color)
    ax[1, 0].spines['right'].set_visible(False)

    for i in range(len(player)):
        ax[1, 0].scatter(x=player['Dribbling Ability'].values[i], y=player['decisionMake'].values[i], s=400, c='#FCAC14', lw=2, edgecolor=background, label=playerName, zorder=3)

    ##############################################################################################

    ax[1, 1].set_facecolor(background)
    ax[1, 1].scatter(x=df['Finishing Ability'], y=df['Heading Ability'], alpha=.1, lw=1, color='#E8E8E8', hatch='///////')
    ax[1, 1].set_title('Finishing vs Heading', color=color, size=18)
    ax[1, 1].axvline(df['Finishing Ability'].mean(), c=color)
    ax[1, 1].axhline(df['Heading Ability'].mean(), c=color)

    ax[1, 1].tick_params(axis='x', colors=color, labelsize=12)
    ax[1, 1].tick_params(axis='y', colors=color, labelsize=12)

    ax[1, 1].spines['bottom'].set_color(color)
    ax[1, 1].spines['top'].set_visible(False)
    ax[1, 1].spines['left'].set_color(color)
    ax[1, 1].spines['right'].set_visible(False)

    for i in range(len(player)):
        ax[1, 1].scatter(x=player['Finishing Ability'].values[i], y=player['Heading Ability'].values[i], s=400, c='#FCAC14', lw=2, edgecolor=background, label=playerName, zorder=3)

##############################################################################################################################################################################

    #Criação da legenda
    l = plt.legend(facecolor=background, framealpha=.05, labelspacing=.9, prop={'size': 10})
    #Ciclo FOR para atribuir a white color na legend
    for text in l.get_texts():
        text.set_color(color)

    fig.suptitle('Offensive Aspects', color=color, size=35)
    return plt.show()

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def radar_chart_compare(df, player, player2, cols, team, season, league, league_Compare, season_Compare):

    if type(season_Compare) != 'str':
            str(season_Compare)
    else:
        pass

    #Obtenção dos dois jogadores que pretendemos
    pl1 = df[(df['Player'] == player) & (df['Team'] == team) & (df['Comp'] == league) & (df['Season'] == season)]

    position = pl1['Main Pos'].unique()[0]

    val1 = pl1[cols].values[0]

    club = pl1['Team'].values[0]
    if club == '0':
            club = 'Jogador livre'

    league = pl1['Comp'].values[0]

    #Obtenção dos dois jogadores que pretendemos
    pl2 = df[(df['Player'] == player2) & (df['Season'] == season)]
    val2 = pl2[cols].values[0]

    position2 = pl2['Main Pos'].unique()[0]

    club2 = pl2['Team'].values[0]
    if club2 == '0':
            club2 = 'Jogador livre'
    league2 = pl2['Comp'].values[0]

    #Obtenção dos valores das colunas que pretendemos colocar no radar chart, não precisamos aceder ao index porque só iriamos aceder aos valores de um dos jogadores
    values = [val1, val2]

    rango = df.loc[(df['League'] == league_Compare)  & (df['Season'] == season_Compare) & (df['Main Pos'] == position)].reset_index(drop=True)

    #Obtençaõ dos valores min e max das colunas selecionadas
    ranges = [(rango[col].min(), rango[col].max()) for col in cols] 

    #Atribuição dos valores aos titulos e respetivos tamanhos e cores
    title = dict(
        #Jogador 1
        title_name = player,
        title_color = '#548135',
        
        #Jogador 2
        title_name_2 = player2,
        title_color_2 = '#fb8c04',

        #Tamnhos gerais do radar chart
        title_fontsize = 20,
        subtitle_fontsize = 15,

        subtitle_name=club,
        subtitle_color='#181818',
        subtitle_name_2=club2,
        subtitle_color_2='#181818',

    )

    #team_player = df[col_name_team].to_list()

    #dict_team ={'Dortmund':['#ffe011', '#000000'],
                #'Nice':['#cc0000', '#000000'],
                #'Nice':['#cc0000', '#000000']}

    #color = dict_team.get(team_player[0])

    ## endnote 
    endnote = "Visualization made by: Pedro Meneses(@menesesp20)"

    #Criação do radar chart
    fig, ax = plt.subplots(figsize=(18,15), dpi=500)
    radar = Radar(background_color="#181818", patch_color="#181818", range_color="#181818", label_color="#181818", label_fontsize=11, range_fontsize=11)
    fig, ax = radar.plot_radar(ranges=ranges, 
                                params=cols, 
                                values=values, 
                                radar_color=['#548135','#fb8c04'], 
                                figax=(fig, ax),
                                title=title,
                                endnote=endnote, end_size=0, end_color="#e9eaea",
                                compare=True)

    fig.set_facecolor('#e9eaea')

    return plt.show()

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def radar_chart(df, player, cols, team, season, league, leagueCompare, season_Compare, number, minutes, minutes_2, player2=None):

    if type(season_Compare) != 'str':
        str(season_Compare)
    else:
        pass

    if player2 == None:
        #Atribuição do jogador a colocar no gráfico
        players = df.loc[(df['Player'] == player) & (df['Team'] == team) & (df['Comp'] == league) & (df['Season'] == season) &
                         ((df['Minutes played'] >= minutes) | (df['Minutes played'] <= minutes_2))].reset_index(drop=True)

        club = players.Team.unique()[0]
        if club == '0':
            club = 'Jogador livre'

        position = players['Main Pos'].unique()[0]

        #####################################################################################################################

        #Valores que pretendemos visualizar no radar chart, acedemos ao index 0 para obtermos os valores dentro da lista correta
        values = players[cols].values[0]
        values = [value * number for value in values]
        #Obtenção do alcance minimo e máximo dos valores

        rango = df.loc[(df['League'] == leagueCompare) & (df['Season'] == season_Compare) & (df['Minutes played'] >= 800) & (df['Main Pos'] == position) | (df.Player == player)].reset_index(drop=True)

        ranges = [(rango[col].min(), rango[col].max()) for col in cols]

        color = ['#181818','#fb8c04']
        #Atribuição dos valores aos titulos e respetivos tamanhos e cores
        title = dict(
            title_name = player,
            title_color = color[0],
            title_fontsize = 20,
            subtitle_fontsize = 10,

            subtitle_name=club,
            subtitle_color='#181818',
        )

        #team_player = df[col_name_team].to_list()

        #dict_team ={'Dortmund':['#ffe011', '#000000'],
                    #'Nice':['#cc0000', '#000000'],}

        #color = dict_team.get(team_player[0])

        ## endnote 
        endnote = "Visualization made by: Pedro Meneses(@menesesp20)"

        #Criação do radar chart
        fig, ax = plt.subplots(figsize=(12,10))
        radar = Radar(background_color="#181818", patch_color="white", range_color="#181818", label_color="#181818", label_fontsize=10, range_fontsize=10)
        fig, ax = radar.plot_radar(ranges=ranges, 
                                    params=cols, 
                                    values=values, 
                                    radar_color=color,
                                    figax=(fig, ax),
                                    image_coord=[0.464, 0.81, 0.1, 0.075],
                                    title=title,
                                    endnote=endnote)

        fig.set_facecolor('#e9eaea')
        # Ensure the 'Images' folder exists
        if not os.path.exists(f'Images/Recruitment/{player}'):
            os.makedirs(f'Images/Recruitment/{player}')

        # Save the figure
        plt.savefig(f'Images/Recruitment/{player}/{player} Percentile.png')

    else:
        radar_chart_compare(df, player, player2, cols, team, season, league, league_Compare_Context, Season_Compare_Context)
        
    return plt.show()

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def PizzaChart(df, cols, playerName, team, season, league, leagueCompare, season_Compare, number, minutes, minutes_2):

    if type(season_Compare) != 'str':
            str(season_Compare)
    else:
        pass

    # parameter list
    params = cols

    playerDF = df.loc[(df.Player == playerName) & (df.Team == team) & (df['Comp'] == league) & (df['Season'] == season)]
    
    position = playerDF['Position'].unique()

    position = position.tolist()

    position = position[0]
    if ', ' in position:
        position = position.split(', ')[0]

    marketValue = playerDF['Market value'].unique()

    marketValue = marketValue.tolist()
    
    marketValue = marketValue[0]

    df = df.loc[(df['League'] == leagueCompare) & ((df['Minutes played'] >= minutes) | (df['Minutes played'] <= minutes_2)) &
                (df['Season'] == season_Compare) & (df['Position'].str.contains(position))].reset_index(drop=True)

    player = playerDF[cols].reset_index()
    player = list(player.loc[0])
    player = player[1:]
    player = [value * number for value in player]

    values = []
    for x in range(len(params)):   
        values.append(math.floor(stats.percentileofscore(df[params[x]], player[x])))

    for n,i in enumerate(values):
        if i == 100:
            values[n] = 99

    if cols == Forward:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 4 + ["#eb04e3"] * 4
        text_colors = ["#181818"] * 11

    elif cols == Winger:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 7 + ["#eb04e3"] * 3
        text_colors = ["#181818"] * 13

    elif cols == defensive_Midfield:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 4 + ["#eb04e3"] * 6
        text_colors = ["#181818"] * 13
        
    elif cols == Midfield:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 8 + ["#eb04e3"] * 3
        text_colors = ["#181818"] * 14

    elif cols == full_Back:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 4 + ["#fb8c04"] * 5 + ["#eb04e3"] * 4
        text_colors = ["#181818"] * 13

    elif cols == center_Back:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 3 + ["#eb04e3"] * 7
        text_colors = ["#181818"] * 13

    elif cols == offensive_Midfield:
        # color for the slices and text
        slice_colors = ["#2d92df"] * 3 + ["#fb8c04"] * 8 + ["#eb04e3"] * 4
        text_colors = ["#181818"] * 15

    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#e9eaea",     # background color
        straight_line_color="#ffffff",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#ffffff",    # color for last line
        last_circle_lw=1,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(12, 8),                # adjust the figsize according to your need
        color_blank_space="same",        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#ffffff", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#181818", fontsize=8,
            va="center"
        ),                               # values to be used when adding parameter labels
        kwargs_values=dict(
            color="#181818", fontsize=8,
            zorder=3,
            bbox=dict(
                edgecolor="#ffffff", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values labels
    )

    if cols == Forward:

        fig_text(s =  'Forward Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)

    elif cols == Winger:

        fig_text(s =  'Winger Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)

    elif cols == defensive_Midfield:

        fig_text(s =  'Defensive Midfield Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)

    elif cols == Midfield:

        fig_text(s =  'Midfield Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)

    elif cols == full_Back:

        fig_text(s =  'Full Back Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)
    elif cols == center_Back:

        fig_text(s =  'Center Back Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)

    elif cols == offensive_Midfield:

        fig_text(s =  'Offensive Midfield Template',
             x = 0.253, y = 0.035,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=6)

    ###########################################################################################################

    fig_text(s =  playerName,
             x = 0.5, y = 1.12,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=40);

    fig_text(s =  'Percentile Rank | ' + league + ' | Pizza Chart | ' + str(season),
            x = 0.5, y = 1.03,
            color='#181818',
            fontweight='bold', ha='center',
            fontsize=12);

    #fig_text(s =  str(marketValue),
    #         x = 0.5, y = 1.02,
    #         color='#181818',
    #         fontweight='bold', ha='center',
    #         fontsize=18);

    # add credits
    CREDIT_1 = "data: WyScout"
    CREDIT_2 = "made by: @menesesp20"
    CREDIT_3 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


    # CREDITS
    fig_text(s =  f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}",
             x = 0.35, y = 0.02,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=8);

    # Attacking
    fig_text(s =  'Attacking',
             x = 0.41, y = 0.988,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=16);

    # Possession
    fig_text(s =  'Possession',
             x = 0.535, y = 0.988,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=16);

    # Defending
    fig_text(s =  'Defending',
             x = 0.665, y = 0.988,
             color='#181818',
             fontweight='bold', ha='center',
             fontsize=16);

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.337, 0.97), 0.025, 0.021, fill=True, color="#2d92df",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.462, 0.97), 0.025, 0.021, fill=True, color="#fb8c04",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.593, 0.97), 0.025, 0.021, fill=True, color="#eb04e3",
            transform=fig.transFigure, figure=fig
        ),
    ])

    # Ensure the 'Images' folder exists
    if not os.path.exists(f'Images/Recruitment/{playerName}'):
        os.makedirs(f'Images/Recruitment/{playerName}')

    # Save the figure
    plt.savefig(f'Images/Recruitment/{playerName}/{playerName} Percentile.png')

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def score_OverTime(df, club, playerName, league, number, colPercentile):
    # plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Set color background outside the graph
    fig.set_facecolor('#e9eaea')

    # Set color background inside the graph
    ax.set_facecolor('#e9eaea')

    ax.tick_params(axis='x', colors='#181818', labelsize=12)
    ax.tick_params(axis='y', colors='#181818', labelsize=12)

    ax.spines['bottom'].set_color('#181818')
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color('#181818')
    ax.spines['right'].set_visible(False)

    league = re.split(' \d{4}', league)[0]

    # Filter the DataFrame
    player = df[
        (df['Player'] == playerName) & 
        (df['Team'] == club)
    ].sort_values('Season', ascending=True).reset_index(drop=True)

    team = player['Team'].unique()[0]
    scores = player[colPercentile].values
    seasons = player['Season'].unique()
    minutes_played = player['Minutes played'].values

    y = scores
    y = [round(value * number, 2) for value in y]
    print('Score:', y)
    x = seasons
    print('\nSeasons: ', x)

    ax.set_ylim([0, 100])

    # Add gridlines
    ax.grid(which='major', axis='y', linestyle='--', color='grey', alpha=0.7)

    ax.plot(x, y, marker='.', markersize=12, c='#FF0000')

    # Annotate each point with its score value and minutes played
    for i, (score, minutes) in enumerate(zip(y, minutes_played)):
        ax.annotate(score, (x[i], y[i]), fontproperties=custom_font, textcoords="offset points", xytext=(0,10), ha='center', color='#181818')
        ax.annotate(f'{minutes} min', (x[i], y[i]), fontproperties=custom_font, textcoords="offset points", xytext=(0,-15), ha='center', color='#181818')

    plt.title(f'{playerName} {team}\nPercentile Over Time', c='#181818', fontproperties=custom_font, fontsize=24, y=1.09)

    plt.ylabel('TOF VALUE', fontproperties=custom_font, color='#181818', size=11)
    plt.xlabel('SEASON', fontproperties=custom_font, color='#181818', size=11)

    fig_Player = add_image(image=f'Images/player_Icon.png', fig=fig, left=0.105, bottom=0.92, width=0.14, height=0.18)
    fig_Club = add_image(image=f'Images/Clubs/Brasileirao/Ceará.png', fig=fig, left=0.79, bottom=0.95, width=0.09, height=0.09)

    # Ensure the 'Images' folder exists
    if not os.path.exists(f'Images/Recruitment/{playerName}'):
        os.makedirs(f'Images/Recruitment/{playerName}')

    # Save the figure
    plt.savefig(f'Images/Recruitment/{playerName}/{playerName} OverTime.png')

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def plotMaps(df, playerName, mode=None):
    if mode == None:
        color = '#E8E8E8'
        background = '#181818'
    elif mode != None:
        color = '#181818'
        background = '#E8E8E8'

    # SUBPLOTS DEFINE ROWS AND COLS
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(25, 15), dpi=500, facecolor = background)

    # FOOTBALL PITCH
    pitch = Pitch(pitch_type='opta',
                  pitch_color=background, line_color=color,
                  line_zorder=1, linewidth=2, spot_scale=0.002)

    # DRAW THE PITCH IN THE FIGURE AXIS
    pitch.draw(ax=ax[0, 0])

    # AXIS TITLE
    ax[0, 0].set_title('Position With Ball', color=color, size=18)

    # DATAFRAME ONLY WITH THE TOUCHES OF THE PLAYER
    player = df.loc[(df['name'] == playerName) & ((df['isTouch'] == True) | (df['typedisplayName'] == 'Pass'))].reset_index(drop=True)

    #####################################################################################################################################

    # GRADIENT COLOR
    pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        [background, '#3d0000', '#ff0000'], N=10)

    # PATH EFFECTS OF THE HEAT MAP
    path_eff = [path_effects.Stroke(linewidth=3, foreground=color),
                path_effects.Normal()]

    # BINS FOR THE HEAT MAP
    bs1 = pitch.bin_statistic_positional(player['x'], player['y'],  statistic='count', positional='full', normalize=True)

    # HEAT MAP POSITIONAL PITCH (WAY OF PLAY FOOTBALL)
    pitch.heatmap_positional(bs1, edgecolors=color, ax=ax[0, 0], cmap=pearl_earring_cmap, alpha=0.6)

    # LABEL HEATMAP
    pitch.label_heatmap(bs1, color=background, fontsize=16,
                                ax=ax[0, 0], ha='center', va='center',
                                str_format='{:.0%}', path_effects=path_eff, zorder=5)

    #filter that dataframe to exclude outliers. Anything over a z score of 1 will be excluded for the data points
    convex = player[(np.abs(stats.zscore(player[['x','y']])) < 1).all(axis=1)]

    hull = pitch.convexhull(convex['x'], convex['y'])

    pitch.polygon(hull, ax=ax[0, 0], edgecolor=background, facecolor=color, alpha=0.2, linestyle='--', linewidth=3, zorder=2)

    pitch.scatter(player['x'], player['y'], ax=ax[0, 0], s=25, edgecolor=color, facecolor=background, linewidth=1.5, alpha=0.3, zorder=2)

    pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=ax[0, 0], c='#FF0000', edgecolor=color, lw=2, s=400, zorder=3)
    
    #####################################################################################################################################
    
    # FOOTBALL PITCH
    pitch = Pitch(pitch_type='opta',
                  pitch_color=background, line_color=color,
                  line_zorder=1, linewidth=2, spot_scale=0.002)

    # DRAW THE PITCH IN THE FIGURE AXIS
    pitch.draw(ax=ax[0, 1])

    # AXIS TITLE
    ax[0, 1].set_title('Position WithOut Ball', color=color, size=18)

    defensiveActions = ['Clearance', 'Interception', 'Aerial', 'BlockedPass', 'Foul', 'Card', 'Challenge', 'Tackle']

    # DATAFRAME ONLY WITH THE TOUCHES OF THE PLAYER
    player = df.loc[(df['name'] == playerName) &
                    ((df['typedisplayName'] == defensiveActions[0]) | (df['typedisplayName'] == defensiveActions[1]) |
                     (df['typedisplayName'] == defensiveActions[2]) | (df['typedisplayName'] == defensiveActions[3]) |
                     (df['typedisplayName'] == defensiveActions[4]) | (df['typedisplayName'] == defensiveActions[5]) |
                     (df['typedisplayName'] == defensiveActions[6]) | (df['typedisplayName'] == defensiveActions[7]))].reset_index(drop=True)

    #####################################################################################################################################

    # GRADIENT COLOR
    pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        [background, '#3d0000', '#ff0000'], N=10)

    # PATH EFFECTS OF THE HEAT MAP
    path_eff = [path_effects.Stroke(linewidth=3, foreground=color),
                path_effects.Normal()]

    # BINS FOR THE HEAT MAP
    bs2 = pitch.bin_statistic_positional(player['x'], player['y'],  statistic='count', positional='full', normalize=True)

    # HEAT MAP POSITIONAL PITCH (WAY OF PLAY FOOTBALL)
    pitch.heatmap_positional(bs2, edgecolors=color, ax=ax[0, 1], cmap=pearl_earring_cmap, alpha=0.6)

    # LABEL HEATMAP
    pitch.label_heatmap(bs2, color=background, fontsize=16,
                                ax=ax[0, 1], ha='center', va='center',
                                str_format='{:.0%}', path_effects=path_eff, zorder=5)

    #filter that dataframe to exclude outliers. Anything over a z score of 1 will be excluded for the data points
    convex = player[(np.abs(stats.zscore(player[['x','y']])) < 1).all(axis=1)]

    hull = pitch.convexhull(convex['x'], convex['y'])

    pitch.polygon(hull, ax=ax[0, 1], edgecolor=background, facecolor=color, alpha=0.2, linestyle='--', linewidth=3, zorder=2)

    pitch.scatter(player['x'], player['y'], ax=ax[0, 1], s=25, edgecolor=color, facecolor=background, linewidth=1.5, alpha=0.3, zorder=2)

    pitch.scatter(x=convex['x'].mean(), y=convex['y'].mean(), ax=ax[0, 1], c='#FF0000', edgecolor=color, lw=2, s=400, zorder=3)
    
    #####################################################################################################################################

    # FOOTBALL PITCH
    pitch = VerticalPitch(pitch_type='opta',
                pitch_color=background, line_color=color,
                line_zorder=1, linewidth=2, spot_scale=0.002)

    # DRAW THE PITCH IN THE FIGURE AXIS
    pitch.draw(ax=ax[1, 0])

    # AXIS TITLE
    ax[1, 0].set_title('Chance Creation', color=color, size=18)

    # DATAFRAME WITH THE CHANCES CREATED BY THE PLAYER
    chances = df.loc[(df['name'] == playerName) & (df['qualifiers'].str.contains('KeyPass') == True)].reset_index(drop=True)

    # GRADIENT COLOR
    pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        [background, '#3d0000', '#ff0000'], N=10)

    # PATH EFFECTS OF THE HEAT MAP
    path_eff = [path_effects.Stroke(linewidth=3, foreground=color),
                path_effects.Normal()]

    # BINS FOR THE HEAT MAP
    bs3 = pitch.bin_statistic_positional(chances['y'], chances['x'],  statistic='count', positional='full', normalize=True)

    # HEAT MAP POSITIONAL PITCH (WAY OF PLAY FOOTBALL)
    pitch.heatmap_positional(bs3, edgecolors=color, ax=ax[1, 0], cmap=pearl_earring_cmap, alpha=0.6)

    # LABEL HEATMAP
    pitch.label_heatmap(bs3, color=background, fontsize=18,
                                ax=ax[1, 0], ha='center', va='center',
                                str_format='{:.0%}', path_effects=path_eff)

    #####################################################################################################################################

    # FOOTBALL PITCH
    pitch = VerticalPitch(pitch_type='opta', half=True,
                pitch_color=background, line_color=color,
                line_zorder=1, linewidth=2, spot_scale=0.002)

    # DRAW PITCH IN THE FIGURE AXIS
    pitch.draw(ax=ax[1, 1])

    # AXIS TITLE
    ax[1, 1].set_title('Key Passes', color=color, size=18)

    # DATAFRAME ONLY WITH THE PASSES OF THE PLAYER
    passes = df.loc[(df['name'] == playerName) & (df['typedisplayName'] == 'Pass') & (df['x'] >= 55)].reset_index(drop=True)

    # DATAFRAME WITHT THE KEY PASSES OF THE PLAYER
    keyPass = passes.loc[(passes['qualifiers'].str.contains('KeyPass') == True)].reset_index(drop=True)

    # DATAFRAME WITHT THE KEY PASSES OF THE PLAYER
    penBox = passes.loc[(passes['endX'] >= 94.2) & ((passes['endY'] >= 36.8) | (passes['endY'] <= 63.2))].reset_index(drop=True)

    # DATAFRAME WITHT THE CROSSES OF THE PLAYER
    cross = passes.loc[(passes['qualifiers'].str.contains('Cross') == True)].reset_index(drop=True)

    ####################################################################################################

    # PASSES INTO PENALTY BOX
    pitch.lines(cross['x'], cross['y'],
                cross['endX'], cross['endY'],
                color = '#EA04DC', alpha=0.5,
                lw=4, transparent=True, comet=True,
                zorder=5, ax=ax[1, 1])

    # FINAL 1/3 SCATTER
    pitch.scatter(cross['x'], cross['y'], s=150,
                marker='o', edgecolors=background, lw=2, c='#EA04DC',
                zorder=5, ax=ax[1, 1], label='Cross')

    ####################################################################################################

    # PASSES INTO PENALTY BOX
    pitch.lines(penBox['x'], penBox['y'],
                penBox['endX'], penBox['endY'],
                color = '#2D92DF', alpha=0.5,
                lw=4, transparent=True, comet=True,
                zorder=5, ax=ax[1, 1])

    # FINAL 1/3 SCATTER
    pitch.scatter(penBox['x'], penBox['y'], s=150,
                marker='o', edgecolors=background, lw=2, c='#2D92DF',
                zorder=5, ax=ax[1, 1], label='Pen box')

    ####################################################################################################

    # KEY PASSES
    pitch.lines(keyPass['x'], keyPass['y'],
                keyPass['endX'], keyPass['endY'],
                color = '#FFBA08', alpha=0.5,
                lw=4, transparent=True, comet=True,
                zorder=5, ax=ax[1, 1])

    # KEY PASS SCATTER
    pitch.scatter(keyPass['x'], keyPass['y'], s=150,
                marker='o', edgecolors=background, lw=2, c='#FFBA08',
                zorder=5, ax=ax[1, 1], label='Key Pass')

    ####################################################################################################

    # PASSES
    pitch.lines(passes['x'], passes['y'],
                passes['endX'], passes['endY'],
                color = color, alpha=0.2,
                lw=4, transparent=True, comet=True, ax=ax[1, 1])

    ####################################################################################################

    # LEGEND
    l = plt.legend(facecolor=background, framealpha=.05, labelspacing=.9, bbox_to_anchor =(0.29, 0.955), ncol = 3, prop={'size': 8})
    # FOR LOOP TO ATTRIBUTE WHITE COLOR TO LEGEND TEXT
    for text in l.get_texts():
        text.set_color(color)
        
    return plt.show()

with st.form("select-buttons"):
    #options_PlayerOPTA = st.sidebar.selectbox(
    #    'Choose Player you want analyse (Event Data)',
    #    sorted(opta.name.unique()))

    options_Player = st.sidebar.selectbox(
        'Choose Player you want analyse',
        wyscout.Player.unique())

    options_Team = st.sidebar.selectbox(
        'Select the players team',
        sorted(wyscout[wyscout['Player'] == options_Player]['Team'].unique()))

    options_Player_Compare = st.sidebar.selectbox(
        'Choose Player you want to compare',
        wyscout.Player.unique())

    leagues_List = wyscout.loc[wyscout.Player == options_Player]['Comp'].unique()

    league_Context = st.sidebar.selectbox(
    'Choose league you want analyse', leagues_List)

    league_Compare_Context = st.sidebar.selectbox(
    'Choose league you to see the player', wyscout['League'].unique())

    Season_Compare_Context = st.sidebar.selectbox(
    'Choose the season from the league to context', wyscout[(wyscout['League'] == league_Compare_Context)]['Season'].unique())

    Season_List = wyscout.loc[wyscout.Player == options_Player]['Season'].unique()

    Season = st.sidebar.selectbox(
    'Choose Season you want analyse', Season_List)

    number_Adjust = st.sidebar.selectbox(
    'Choose value to adjust the player scores', [1, 0.95, 0.93, 0.90, 0.88, 0.82, 0.85, 0.80, 0.78, 0.75])

    page_width_user = st.sidebar.selectbox(
    'Choose width value', list(range(10, 31)))

    page_height_user = st.sidebar.selectbox(
    'Choose height value', list(range(10, 31)))

    minutes_Lower = st.sidebar.selectbox(
    'Set minimum minutes', list(range(0, 30000)))

    minutes_Max = st.sidebar.selectbox(
    'Set maximium minutes', list(range(0, 30000)))

    score_Adjusted = st.sidebar.selectbox(
                    'Has the score been already adjusted?', ['No', 'Yes'])

    if score_Adjusted == 'No':
            number_Adjust = st.sidebar.selectbox(
                    'Choose value to adjust the player scores', [1, 0.95, 0.93, 0.90, 0.88, 0.85, 0.82, 0.80, 0.78, 0.75])
            score_column = 'Score'
    else:
            number_Adjust = 1
            score_column = 'AdjustedScore'

    #wyscout = wyscout[(wyscout['Season'] == Season)].reset_index(drop=True)

    cols = st.sidebar.selectbox('Choose the template for the radars',
                                ['Center Back', 'Full Back', 'Defensive Midfield', 'Midfield', 'Offensive Midfield', 'Winger', 'Forward'])

    if cols == 'Center Back':
        cols = center_Back
    elif cols == 'Full Back':
        cols = full_Back
    elif cols == 'Defensive Midfield':
        cols = defensive_Midfield
    elif cols == 'Midfield':
        cols = Midfield
    elif cols == 'Offensive Midfield':
        cols = offensive_Midfield
    elif cols == 'Winger':
        cols = Winger
    elif cols == 'Forward':
        cols = Forward

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    btn1 = col1.form_submit_button(label='Bars')
    btn2 = col2.form_submit_button(label='Scatters')
    btn3 = col3.form_submit_button(label='Radar')
    btn4 = col4.form_submit_button(label='Radar Compare')
    btn5 = col5.form_submit_button(label='Percentile')
    btn6 = col6.form_submit_button(label='Progress Over Time')

#col1, col2, col3, col4, col5, col6 = st.columns(6)

if btn1:
        figBars = barsAbility(wyscout, options_Player, options_Team, Season, league_Context, league_Compare_Context, Season_Compare_Context, number_Adjust, minutes_Lower, minutes_Max)
        st.pyplot(figBars)

if btn2:
    figScatters = Scatters(data, options_Player, options_Team)
    
    st.pyplot(figScatters)

if btn3:

    figRadar = radar_chart(wyscout, options_Player, cols, options_Team, Season, league_Context, league_Compare_Context, Season_Compare_Context, number_Adjust, minutes_Lower, minutes_Max)
    
    st.pyplot(figRadar)

if btn4:
    figRadarCompare = radar_chart(wyscout, options_Player, cols, options_Team, Season, league_Context, league_Compare_Context, Season_Compare_Context, options_Player_Compare)
    
    st.pyplot(figRadarCompare)

if btn5:

    figPercentile = PizzaChart(wyscout, cols, options_Player, options_Team, Season, league_Context, league_Compare_Context, Season_Compare_Context, number_Adjust, minutes_Lower, minutes_Max)
    
    st.pyplot(figPercentile)

if btn6:
    figOverTime = score_OverTime(wyscout, options_Team, options_Player, league_Context, number_Adjust, score_column)

    st.pyplot(figOverTime)

def sort_images(files):
    order = ['Report', 'Bars', 'Radar', 'Percentile', 'OverTime']
    files.sort(key=lambda x: next((i for i, keyword in enumerate(order) if keyword in x), len(order)))
    return files

def createReportPDF(playerName, leagueName, uploaded_files, page_width=20, page_height=15):
    def inch_to_px(value):
        return value * 72

    def resize_image(image_path, max_width, max_height):
        with open(image_path, "rb") as img_file:
            img = PILImage.open(img_file)
            img.thumbnail((max_width, max_height))
            return img

    def create_pdf_report(image_paths, playerName, leagueName, page_width, page_height):
        local_reports_dir = 'Reports'
        if not os.path.exists(local_reports_dir):
            os.makedirs(local_reports_dir)

        pdf_path = os.path.join(local_reports_dir, f'{playerName} Report.pdf')
        doc = BaseDocTemplate(pdf_path, pagesize=landscape((inch_to_px(page_width), inch_to_px(page_height))), showBoundary=0)

        margin = 20
        frame_width = inch_to_px(page_width) - 2 * margin
        frame_height = inch_to_px(page_height) - 2 * margin
        frame = Frame(margin, margin, frame_width, frame_height)

        def draw_background(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(colors.HexColor("#e9eaea"))
            canvas.rect(0, 0, inch_to_px(page_width), inch_to_px(page_height), fill=True, stroke=False)
            canvas.restoreState()

        page_template = PageTemplate(frames=frame, onPage=draw_background)
        doc.addPageTemplates([page_template])

        elements = []

        sorted_image_paths = sort_images(image_paths)

        for img_path in sorted_image_paths:
            img = resize_image(img_path, frame_width, frame_height)
            img_width, img_height = img.size
            centered_y = (frame_height - img_height) / 2
            if elements:  # Add a spacer for all but the first image
                elements.append(Spacer(1, centered_y))
            elements.append(Image(img_path, width=img_width, height=img_height))
            elements.append(PageBreak())

        doc.build(elements)

    create_pdf_report(uploaded_files, playerName, leagueName, page_width, page_height)

# Initialize session state variables if not already done
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []
if 'pdf_generated' not in st.session_state:
    st.session_state['pdf_generated'] = False

# Step 1: Implement File Upload
uploaded_files = st.file_uploader("Upload Images for the Report", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

# Process uploaded files
if uploaded_files:
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    st.session_state['uploaded_files'] = []

    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            bytes_data = uploaded_file.read()
            image_path = os.path.join(temp_dir, uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(bytes_data)
            st.session_state['uploaded_files'].append(image_path)

# Step 2: Create PDF Report Button
if st.button('Create PDF Report'):
    if st.session_state['uploaded_files']:
        createReportPDF(options_Player, league_Context, st.session_state['uploaded_files'], page_width_user, page_height_user)
        st.session_state['pdf_generated'] = True

# Step 3: Provide download button if PDF has been generated
if st.session_state['pdf_generated']:
    pdf_path = f'Reports/{options_Player} Report.pdf'
    try:
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name=f"{options_Player}_Report.pdf",
                mime="application/octet-stream"
            )
        st.success('Your report has been generated. Click the button above to download.')
    except IOError:
        st.error('An error occurred while generating the report.')

