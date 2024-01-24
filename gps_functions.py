# Libraries for data handling and manipulation
import pandas as pd
import numpy as np

import math

# Libraries for visualizations
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

# Libraries for signal processing
from scipy.signal import butter, lfilter

# Libraries for spatial calculations
from scipy.spatial import ConvexHull, distance

import os

reference_points = {
    'A': (-3.745538,-38.537283),
    'B': (-3.746451,-38.537013),
    'C': (-3.746260,-38.536374),
    'D': (-3.745349,-38.536644)
}

# Função para o filtro Butterworth passa-baixa
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

def convert_to_cartesian(lat, long):
    def map_from_to(x, a, b, c, d):
        y = (x - a) / (b - a) * (d - c) + c
        return y
    x = map_from_to(long, reference_points['A'][1], reference_points['C'][1], 0, 68)
    y = map_from_to(lat, reference_points['A'][0], reference_points['B'][0], 0, 105)
    return x, y

def concat_data(files, cutoff_frequency, sampling_frequency, order):
    lista_df = []
    for file in files:
        df = pd.read_csv(f'/content/drive/MyDrive/GPS/Heatmap Jogos 2023/22.10.2023 - Avaí x Ceará/{file}', skiprows=8, delimiter=';', decimal=",")
        lista_df.append(df)

    data = pd.concat(lista_df, axis=0)

    data['Y'], data['X'] = zip(*data.apply(lambda row: convert_to_cartesian(row['Latitude'], row['Longitude']), axis=1))
    if not isinstance(data['Timestamp'].iloc[0], pd.Timestamp):
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    data['X_filtered'] = butter_lowpass_filter(data['X'], cutoff_frequency, sampling_frequency, order)
    data['Y_filtered'] = butter_lowpass_filter(data['Y'], cutoff_frequency, sampling_frequency, order)

    return data

def run_map_players(files, players_to_analyze, game_start, game_end, pitch_length, pitch_width):
    # Análise do jogo
    filtered_files = [file for file in files if any(player in file for player in players_to_analyze)]
    for half, start_time, end_time in [('Primeiro Tempo', game_start, game_end)]:
        fig, axes = plt.subplots((len(filtered_files) + 3) // 4, 4, figsize=(20, 20))
        for ax, file in zip(axes.flatten(), filtered_files):

            player_name = file.split("for ")[1].split(".")[0]

            data = pd.read_csv(os.path.join('Data/GPS', file), skiprows=8, delimiter=";", decimal=",")

            data['Y'], data['X'] = zip(*data.apply(lambda row: convert_to_cartesian(row['Latitude'], row['Longitude']), axis=1))

            if not isinstance(data['Timestamp'].iloc[0], pd.Timestamp):
                data['Timestamp'] = pd.to_datetime(data['Timestamp'])

            half_data = data[(data['Timestamp'] >= start_time) & (data['Timestamp'] <= end_time)]

            # Plotagem
            pitch = Pitch(pitch_type='custom', line_color='black', pitch_color='white', stripe=False,
                        pitch_length=pitch_length, pitch_width=pitch_width)
            
            pitch.draw(ax=ax)

            sns.scatterplot(data=half_data, x='X_filtered', y='Y_filtered', ax=ax, color="black", linewidth=0.2, alpha=0.5)

            ax.set_title(player_name)

        # Removendo os gráficos vazios
        for i in range(len(filtered_files), len(axes.flatten())):
            axes.flatten()[i].axis('off')

        plt.suptitle(f'Rastros dos jogadores - {half}', fontsize=20)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

def sprints_Map_Team(data, pitch_length, pitch_width):
    # Análise do jogo Coletiva
    fig, ax = plt.subplots(figsize=(18, 14), dpi=300)

    fig.set_facecolor('#181818')
    # Plotagem
    pitch = Pitch(pitch_type='custom', line_color='white', pitch_color='#181818',
                    stripe=False, pitch_length=pitch_length, pitch_width=pitch_width)
    
    pitch.draw(ax=ax)
    # Plot the completed passes
    pitch.arrows(data['X_filtered'], data['Y_filtered'],
                data['endX'], data['endY'], width=2,
                headwidth=10, headlength=10, color='white', ax=ax)

    ax.set_title('Game Against Mirassol - Win', size=18, color='white')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def sprints_Map_Player(data, pitch_length, pitch_width):
    
    # Group data by PlayerID
    grouped_data = data.groupby('playerName')

    # Number of players and calculating rows for the subplot grid
    num_players = len(grouped_data)
    num_rows = math.ceil(num_players / 3)

    # Create a figure with subplots in a 4x4 grid
    fig, axs = plt.subplots(num_rows, 3, figsize=(18 * 3, 14 * num_rows), dpi=300)
    fig.set_facecolor('#181818')

    # Flatten the axs array for easy iteration
    axs = axs.flatten()

    # Iterate and plot for each player
    for ax, (player_id, group) in zip(axs, grouped_data):
        # Create the pitch on the current subplot
        pitch = Pitch(pitch_type='custom', line_color='white', pitch_color='#181818', 
                    stripe=False, pitch_length=pitch_length, pitch_width=pitch_width)
        pitch.draw(ax=ax)

        # Plot sprints for the player
        pitch.arrows(group['X_filtered'], group['Y_filtered'],
                    group['endX'], group['endY'], width=2,
                    headwidth=10, headlength=10, color='white', ax=ax)

        # Setting the title with player's name
        ax.set_title(f'Sprints Against Mirassol - {player_id}', size=50, color='white')

    # If there are empty subplots, hide them
    for i in range(num_players, len(axs)):
        axs[i].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def heatMap_GPS_Team(data, pitch_length, pitch_width):

        # Análise do jogo Coletiva
        fig, ax = plt.subplots(figsize=(18, 14), dpi=300)

        fig.set_facecolor('#181818')
        # Plotagem
        pitch = Pitch(pitch_type='custom', line_color='white', pitch_color='#181818',
                        stripe=False, pitch_length=pitch_length, pitch_width=pitch_width)
        
        pitch.draw(ax=ax)

        # KDE Plot para o mapa de calor
        sns.kdeplot(data=data, x='X_filtered', y='Y_filtered', ax=ax, cmap='Reds', fill=True, alpha=0.5)

        ax.set_title('Game Against Mirassol - Win', size=18, color='white')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

def heatMap_GPS_Player(data, pitch_length, pitch_width):
    
        # Group data by PlayerID
        grouped_data = data.groupby('playerName')

        # Number of players and calculating rows for the subplot grid
        num_players = len(grouped_data)
        num_rows = math.ceil(num_players / 3)

        # Create a figure with subplots in a 4x4 grid
        fig, axs = plt.subplots(num_rows, 3, figsize=(10 * 3, 8 * num_rows), dpi=300)
        fig.set_facecolor('#181818')

        # Flatten the axs array for easy iteration
        axs = axs.flatten()

        # Iterate and plot for each player
        for ax, (player_id, group) in zip(axs, grouped_data):
            # Create the pitch on the current subplot
            pitch = Pitch(pitch_type='custom', line_color='white', pitch_color='#181818', 
                        stripe=False, pitch_length=pitch_length, pitch_width=pitch_width)
            pitch.draw(ax=ax)

            # KDE Plot para o mapa de calor
            sns.kdeplot(data=group, x='X_filtered', y='Y_filtered', ax=ax, cmap='Reds', fill=True, alpha=0.5)

            # Setting the title with player's name
            ax.set_title(f'Heat Map Against Mirassol - {player_id}', size=25, color='white')

        # If there are empty subplots, hide them
        for i in range(num_players, len(axs)):
            axs[i].axis('off')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

def convexHull_GPS(files, players_to_analyze, game_start, game_end, pitch_length, pitch_width, goalkeeperName):

    # Nome do goleiro a ser excluído da área de ocupação
    goalkeeper_name = goalkeeperName

    # Defina manualmente os jogadores para cálculo da largura e profundidade
    width_players = ['Castilho G', 'Paulo V']
    depth_players = ['Lucas R', 'Saulo R']

    # Filtrando os jogadores
    filtered_files = [file for file in files if any(player in file for player in players_to_analyze)]
    player_avg_positions = {}

    # Coleta as posições médias dos jogadores
    for file in filtered_files:
        try:
            data = pd.read_csv(os.path.join('Data/GPS', file), skiprows=8, delimiter=";", decimal=",")
            player_name = file.split("for ")[1].split(".")[0]
            data['Y'], data['X'] = zip(*data.apply(lambda row: convert_to_cartesian(row['Latitude'], row['Longitude']), axis=1))
            if not isinstance(data['Timestamp'].iloc[0], pd.Timestamp):
                data['Timestamp'] = pd.to_datetime(data['Timestamp'])

            half_data = data[(data['Timestamp'] >= game_start) & (data['Timestamp'] <= game_end)]
            avg_x, avg_y = half_data['X'].mean(), half_data['Y'].mean()

            player_avg_positions[player_name] = (avg_x, avg_y)
        except Exception as e:
            print(f"Erro ao processar o arquivo {file}. Erro: {e}")

    # Calculando largura e profundidade
    width = distance.euclidean(player_avg_positions[width_players[0]], player_avg_positions[width_players[1]])
    depth = distance.euclidean(player_avg_positions[depth_players[0]], player_avg_positions[depth_players[1]])

    # Plotagem
    pitch = Pitch(pitch_type='custom', line_color='black', pitch_color='#aabb97', stripe=False, pitch_length=pitch_length, pitch_width=pitch_width)
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plotando jogadores com marcador preto
    for player_name, position in player_avg_positions.items():
        ax.scatter(position[0], position[1], s=250, c='black', edgecolors='gray', linewidths=0.5)
        ax.text(position[0], position[1] + 2.5, player_name, fontsize=8, ha='center', va='center')

    # Desenhando a largura e profundidade
    ax.plot([player_avg_positions[width_players[0]][0], player_avg_positions[width_players[1]][0]],
            [player_avg_positions[width_players[0]][1], player_avg_positions[width_players[1]][1]], "g--")
    ax.plot([player_avg_positions[depth_players[0]][0], player_avg_positions[depth_players[1]][0]],
            [player_avg_positions[depth_players[0]][1], player_avg_positions[depth_players[1]][1]], "b--")

    # Calculando e desenhando a área de ocupação sem o goleiro especificado
    points_without_goalkeeper = [pos for name, pos in player_avg_positions.items() if name != goalkeeper_name]
    hull = ConvexHull(points_without_goalkeeper)
    hull_area = hull.volume
    hull_points = np.array(points_without_goalkeeper)[hull.vertices]
    ax.fill(hull_points[:,0], hull_points[:,1], color='red', alpha=0.3)  # Preenchendo a área

    # Adicionando as informações no campo
    info_str = (f"Largura: {width:.2f}m\n"
                f"Profundidade: {depth:.2f}m\n"
                f"Área: {hull_area:.2f}m²")
    ax.text(5, 5, info_str, bbox=dict(facecolor='white', alpha=0.5), fontsize=8)

    plt.show()































