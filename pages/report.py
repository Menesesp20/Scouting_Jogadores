import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt
import datetime

from matplotlib import font_manager
import scipy.stats as stats

from highlight_text import  ax_text

from soccerplots.utils import add_image

import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import os
import warnings
warnings.filterwarnings("ignore")

font_path = './Fonts/Lato-Black.ttf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

# Courier New
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.header('Data Report')

@st.cache_data(ttl=86400)
def load_data(filePath):
    wyscout = pd.read_parquet(filePath)
    return wyscout

wyscout = load_data('./Data/wyscout.parquet')

st.cache_data(ttl=datetime.timedelta(hours=1), max_entries=1000)
def traditionalReport(data, league, playerName, team, league_Player, season, score_column, number, minutes, minutes_2, role_Selected=None, mode=None):
        ############################################################################# PLAYER'S ABILITY PERCENTILE #####################################################################################################################################################################################################################################

        data['Habilidade Defensiva'] = data['Habilidade Defensiva'].apply(lambda x: math.floor(stats.percentileofscore(data['Habilidade Defensiva'], x)))

        data['crossing'] = data['crossing'].apply(lambda x: math.floor(stats.percentileofscore(data['crossing'], x)))

        data['defending1v1'] = data['defending1v1'].apply(lambda x: math.floor(stats.percentileofscore(data['defending1v1'], x)))

        data['touchQuality'] = data['touchQuality'].apply(lambda x: math.floor(stats.percentileofscore(data['touchQuality'], x)))

        data['positioning Midfield'] = data['positioning Midfield'].apply(lambda x: math.floor(stats.percentileofscore(data['positioning Midfield'], x)))

        data['runs'] = data['runs'].apply(lambda x: math.floor(stats.percentileofscore(data['runs'], x)))

        ############################################################################# PLAYER'S PROFILES #####################################################################################################################################################################################################################################
        
        stopper = ['Um zagueiro central com grande habilidade para disputar duelos e uma presença física muito forte.\nDevidamente disciplinado, com forte posicionamento defensivo, encurta o espaço para os atacantes bem,\nbloqueando suas tentativas de finalização.']
        
        aerialCB = ['Zagueiro central dominante no ar, domina completamente o espaço dentro da área,\nforte posicionamento defensivo, taticamente disciplinado.']

        ballPlayingCB = ['Zagueiro central com a qualidade de assumir a responsabilidade de construir o jogo\nda equipe desde a defesa, capaz de romper a linha de pressão 1/2 do adversário,\nforte defensivamente em duelos de antecipação com sua visão de jogo.']

        ballCarryingCB = ['Um zagueiro central com qualidade com a bola nos pés, justo, a combinação de suas\nduas principais características faz seu ponto mais forte a capacidade de progredir\ncom a bola sob controle, quebrando as linhas de pressão 1/2 do adversário através de\nsua condução de bola.']

        ##################################################################################################################################################################################################################################################################################################################

        fullBackCB = ['Versátil nas funções que desempenha em campo, capaz de jogar como zagueiro central em uma linha de 3\nna qual desempenha o papel de um centro solto, forte no\npasse vertical alcançando queimar as linhas de pressão 1/2 do adversário,\ntambém cumpre com qualidade o papel de um lateral mais defensivo em uma linha de 4.']

        DefensiveFB = ['Lateral menos avançado, bom posicionamento na cobertura de seus colegas parando\nataques em transição, forte reação à perda da bola.']

        AttackingFB = ['Jogador rápido com a capacidade de atacar a linha de fundo, jogador resistente que\npode jogar o jogo inteiro com grande capacidade física, driblador muito forte que\ndesequilibra seus oponentes diretos, boa colocação de cruzamentos.']

        WingBack = ['Lateral versátil pode jogar em uma linha de 3 ou 4, capacidade física para cobrir toda\na zona lateral, fisicamente forte, excelente habilidade de cruzamento, bom ataque ao espaço.']

        InvertedWingBack = ['Lateral com presença dominante em zonas interiores, excelente habilidade técnica e\nde passe, consiste em superar as linhas de pressão 1/2 do adversário através de sua\ncondução com movimentos de fora para dentro, forte na cobertura defensiva.']

        ##################################################################################################################################################################################################################################################################################################################

        ballWinner = ['Um meio-campista muito forte na recuperação de bola, forte na cobertura defensiva\nde seus companheiros, boa capacidade de pressionar imediatamente após perder a bola,\nforte em duelos onde aproveita muito bem sua habilidade física.']

        deepPlaymaker = ['Ele é o construtor da equipe na defesa, desempenha o papel principal na transição da\ndefesa para o ataque, tem excelente visão e é capaz de acelerar o jogo com passes\npara frente ou para limpar o lado da bola usando variações de flanco.']

        attackPlaymaker = ['Referência de criação no terço final, assume a responsabilidade de encontrar ou criar os espaços\npara a equipe criar perigo, técnico, excelente comando de bolo e primeiro toque.']

        boxToBox = ['Fisicamente forte, grande capacidade de cobrir o terreno central, forte na cobertura defensiva de seus companheiros,\nbom posicionamento permitindo-lhe chegar\nprimeiro a interceptar adversários, forte no momento da pressão.']

        medioGoleador = ['Facilidade de chegar à zona de finalização, jogador dinâmico, se move muito bem\nem zonas avançadas, forte no ataque ao espaço e atrás da linha defensiva, forte na finalização.']

        ##################################################################################################################################################################################################################################################################################################################

        banda = ['Corredor, forte em duelos um contra um, com sua habilidade de driblar sai muito bem\ndessas situações, bom tomador de decisões no terço final 1/3.']
        
        porDentro = ['Ocupa espaços interiores, jogador dinâmico faz muito movimento de fora para dentro\ncom a bola controlada, chegando a zonas de finalização frontal, boa colocação de chutes,\nse move muito bem sem a bola também,\nabre espaço para o lateral atacar a linha de fundo.']

        defensivo = ['Desempenha tarefas mais defensivas dando o equilíbrio necessário para os\njogadores mais ofensivos executarem suas tarefas, bom conhecimento do jogo,\nboa leitura do jogo antecipando e desarmando os adversários,\nrápido nos momentos de transição, forte em antecipar cruzamentos.']

        falso = ['Sua posição é mais interior com mobilidade pela zona interlinha mas também\ncom movimentos de dentro para fora com o lateral, chegando às zonas de finalização,\natacando o espaço com boa qualidade de finalização.']

        ##################################################################################################################################################################################################################################################################################################################

        boxForward = ['Finalizador puro, jogador de área, movimenta-se muito bem dentro da área\nescondendo-se no lado cego do defensor atacando o espaço para finalizar, forte na\nresposta a cruzamentos.']

        false9 = ['Atacante dinâmico, forte no jogo de costas para o gol procurando combinações de 1-2\ncom seus colegas, arrasta consigo marcadores defensores para abrir espaço atrás\npara os alas/meias atacarem a profundidade.']

        targetMan = ['Um jogador referência dentro da área, fisicamente forte e usando isso para vencer os duelos,\nmuito forte no ar, excelente cabeceador, habilidade de vencer o duelo, para \n segurar e tocar no companheiro de equipe.']

        advancedForward = ['Atacante móvel, seja jogando em espaços interiores de costas para o gol procurando\ncombinações entre linhas ou fazendo movimentos de dentro para fora para aparecer\nmais em zonas de corredor, abrindo espaço para seus colegas avançarem pelo espaço interior.']

        ############################################################################# PLAYER'S ABILITY ANALYSIS #####################################################################################################################################################################################################################################

        passing = ['• Jogador com uma qualidade de passe muito boa e\numa ampla gama de opções de passe',
                '• Jogador apresenta uma qualidade de passe muito boa',
                '• Jogador tem uma boa qualidade de passe',
                '• No capítulo de passe, o jogador precisa melhorar um pouco a precisão nas decisões,\nassim como a variabilidade no passe (curto, médio, longo)']
        
        keyPassing = ['• Excelente tomada de decisão, calmo ao decidir',
                '• Muito bom na tomada de decisões',
                '• Às vezes tem momentos de clareza ao tomar decisões']

        setPieces = ['• Especialista em bolas paradas',
                '• Boa qualidade na execução de bolas paradas']

        dribbling = ['• Habilidade de sair de duelos através de dribles, grande qualidade técnica',
                '• Boa habilidade de usar a técnica para driblar seus adversários',
                '• Boa habilidade de drible',
                '• Drible não é seu ponto mais forte']
        
        createChances = ['• Jogador importante na criação de oportunidades graças à sua boa visão,\né capaz de encontrar espaço para seus companheiros de equipe',
                        '• Jogador muito forte na criação de oportunidades e\nfacilmente encontra seus colegas no último 1/3',
                        '• Precisa melhorar, mas tem a qualidade para se tornar um bom jogador no final 1/3']
        
        visaoJogo = ['• Excelente visão de jogo através de sua habilidade de criar o espaço necessário\npara sua equipe progredir em campo e criar situações de gol',
                        '• Facilidade para colocar sua equipe em zonas mais avançadas\ndo campo devido à sua boa capacidade de visão em\nencontrar os espaços e colocar a bola no momento certo',
                        '• Boa visão de jogo, mas precisa correr um pouco mais de risco em suas decisões',
                        '• Precisa melhorar sua habilidade de ver o jogo de frente\npara melhorar suas decisões durante o jogo']

        concentration = ['• Muito focado durante todo o jogo, consegue antecipar facilmente seus oponentes diretos através de sua concentração e está sempre bem posicionado para chegar aos duelos primeiro',
                        '• Um senso do espaço ao seu redor permite que ele vença a maioria de seus duelos diretos desarmando e desabilitando seus oponentes',
                        '• Tem momentos durante o jogo em que perde um pouco de concentração, levando-o a chegar tarde a alguns duelos',
                        '• Precisa melhorar seu foco no jogo durante os 90 minutos para que possa ser um jogador mais consistente']

        finishing = ['• Finalizador muito forte, não precisa de muitas oportunidades para marcar um gol',
                        "• Jogador com tranquilidade na hora de encontrar o fundo das redes, não precisa de muito para finalizar",
                        '• Boa qualidade na finalização, mas às vezes não mostra tranquilidade no momento cara a cara com o goleiro',
                        "• Habilidade de finalização não é o ponto forte do jogador, precisa evoluir nesse momento do jogo"]

        heading = ['• Responde bem a cruzamentos, excelente cabeceador',
                '• Forte em duelos aéreos, bom cabeceador']

        aerial = ['• Muito forte em duelos aéreos, muito boa habilidade de impulsão',
                '• Agressivo em duelos aéreos, boa habilidade de impulsão',
                '• Precisa melhorar um pouco nos duelos, especialmente os aéreos',
                '• Tem algumas dificuldades em duelos aéreos']

        defensive = ['• No momento defensivo, ele é um jogador muito bom, forte em disputas, forte na habilidade de ler o jogo e antecipar seus oponentes',
                        '• Muito forte no momento defensivo com boa leitura de jogo, permitindo-lhe chegar primeiro aos duelos',
                        '• Precisa melhorar um pouco sua habilidade defensiva']

        crossing = ['• Muita qualidade na hora de cruzar',
                '• Jogador com boa qualidade de cruzamento',
                '• Tem que melhorar a qualidade nos cruzamentos']

        defending1v1 = ['• Muito forte em movimentos defensivos 1x1, forte em manter a posição no momento certo para atacar a bola',
                        '• Boa qualidade defensiva em duelos 1x1, segura bem a posição',
                        '• Precisa melhorar no 1x1 com seus oponentes e entender melhor o momento de atacar a bola']

        positioningDefensive = ['• Posicionamento defensivo irrepreensível, no momento sem a bola é um jogador muito forte',
                                '• Confortável no momento sem a bola, muito bom posicionamento defensivo na marcação de seus oponentes individualmente',
                                '• Tem que melhorar no momento do jogo sem a bola']

        positioningMidfield = ['• Posicionamento defensivo irrepreensível, no momento sem a bola é um jogador muito forte, excelente cobertura defensiva a seus colegas, forte na marcação de seus oponentes individualmente e no bloqueio de linhas de passe',
                                '• Confortável no momento sem a bola, muito bom posicionamento defensivo na marcação de seus oponentes individualmente e no bloqueio de linhas de passe',
                                '• Tem que melhorar no momento do jogo sem a bola']

        progressiveRuns = ['• Excelente capacidade progressiva com bola controlada, queima as linhas defensivas do adversário através de sua qualidade de progressão com bola controlada',
                        '• Boa progressão com a bola no pé, ultrapassa vários jogadores usando seu físico e velocidade para superá-los na progressão com a bola',
                        '• Aspecto a ser melhorado em seu jogo é a progressão com a bola']

        runsOffBall = ['• Jogador muito forte no ataque ao espaço, se move muito bem no campo',
                        "• Se move bem, ataca bem o espaço, mas poderia fazê-lo mais frequentemente e não o faz",
                        '• Jogador um tanto estático em campo, precisa se mover mais, atacar mais o espaço']

        decisionMake = ['• Tomador de decisões muito forte quando está no final 1/3, é um jogador muito perigoso, pode criar uma chance de gol a qualquer momento',
                        '• Jogador muito bom para decidir na última ação',
                        "• Às vezes, no final 1/3, não toma as melhores decisões",
                        '• Precisa melhorar sua tomada de decisão']
        
        touchQual = ['• Excelente primeiro toque',
                '• Bom primeiro toque',
                '• Precisa melhorar seu primeiro toque']

        ############################################################################# ASSIGN PROFILE'S #####################################################################################################################################################################################################################################

        def assign_profile(role):
                if role == 'Zagueiro Bloqueador':
                        return stopper
                elif role == 'Zagueiro Aéreo':
                        return aerialCB
                elif role == 'Zagueiro Construtor de Jogo':
                        return ballPlayingCB
                elif role == 'Zagueiro com Condução de Bola':
                        return ballCarryingCB
                
                elif role == 'Lateral Zagueiro':
                        return fullBackCB
                elif role == 'Lateral Defensivo':
                        return DefensiveFB
                elif role == 'Lateral Ofensivo':
                        return AttackingFB
                elif role == 'Lateral-Ala':
                        return WingBack
                elif role == 'Lateral Invertido':
                        return InvertedWingBack
                
                elif role == 'Volante de Recuperação de Bola':
                        return ballWinner
                elif role == 'Meio-campista Box-to-box':
                        return boxToBox
                elif role == 'Volante Construtor de Jogo':
                        return deepPlaymaker
                elif role == 'Meio-campista Ofensivo':
                        return attackPlaymaker
                elif role == 'Meia de Ligação (Número 10)':
                        return medioGoleador
                
                elif role == 'Ponta Aberto':
                        return banda
                elif role == 'Ponta Interior':
                        return porDentro
                elif role == 'Falso':
                        return falso
                elif role == 'Defensivo':
                        return defensivo
                
                elif role == 'Artilheiro':
                        return boxForward
                elif role == 'Atacante Móvel':
                        return advancedForward
                elif role == 'Falso 9':
                        return false9
                elif role == 'Homem-Referência':
                        return targetMan
                
                else:
                        return 'Função não atribuida'
                
        def assign4(value, profiles):
                if value >= 90:
                        return profiles[0]
                elif (value >= 80) & (value < 90):
                        return profiles[1]
                elif (value >=70) & (value < 80):
                        return profiles[2]
                elif (value >= 40) & (value < 70):
                        return profiles[3]
                elif value < 40:
                        return 'Nada a reportar'

        def assign3(value, profiles):
                if value >= 85:
                        return profiles[0]
                elif (value >= 75) & (value < 85):
                        return profiles[1]
                elif (value >=60) & (value < 75):
                        return profiles[2]
                elif value < 60:
                        return 'Nada a reportar'

        def assign2(value, profiles):
                if value >= 85:
                        return profiles[0]
                elif (value >= 75) & (value < 85):
                        return profiles[1]
                elif value < 75:
                        return 'Nada a reportar'

        def createSkillProfiles(data):
                data['Chances Profile'] = data['Habilidade Criar Chances'].apply(lambda x: assign3(x, createChances))
                data['Touch Profile'] = data['touchQuality'].apply(lambda x: assign3(x, touchQual))
                data['SetPieces Profile'] = data['Habilidade Bola Parada'].apply(lambda x: assign2(x, setPieces))
                data['Decision Profile'] = data['Tomada de decisão'].apply(lambda x: assign4(x, decisionMake))
                data['KeyPass Profile'] = data['Habilidade Passe Decisivo'].apply(lambda x: assign3(x, keyPassing))
                data['OffBall Profile'] = data['runs'].apply(lambda x: assign3(x, runsOffBall))
                data['SightPlay Profile'] = data['Visão de Jogo'].apply(lambda x: assign4(x, visaoJogo))
                data['dribbling Profile'] = data['Habilidade Drible'].apply(lambda x: assign3(x, dribbling))
                data['Pass Profile'] = data['Habilidade Passe'].apply(lambda x: assign4(x, passing))
                data['Player Profile'] = data['Role'].apply(lambda x: assign_profile(x))
                data['Concentration Profile'] = data['Concentração'].apply(lambda x: assign4(x, concentration))

                # Drop columns that contains certain types in his column names
                data.drop(list(data.filter(regex='Unnamed: 0')), axis=1, inplace=True)
                data.drop(list(data.filter(regex='rank_rank')), axis=1, inplace=True)
                
                return data

        data2 = createSkillProfiles(data)

        def report(playerName, league, team, league_Player, mode=None):
                
                if mode == None:
                        color = '#181818'
                        background = '#e9eaea'
                elif mode != None:
                        color = '#181818'
                        background = '#e9eaea'
                        
                df = data2.loc[(data2['Player'] == playerName) &
                               (data2['Team'] == team) &
                               (data2['League'] == league_Player) &
                               (data2['Season'] == season)].reset_index()
                
                country = df['Birth country'].unique()[0]
                if country == '0':
                        country = df['Passport country'].unique()
                        country = country.tolist()
                        country = country[0]
                if ',' in country:
                        country = country.split(', ')[0]

                Market = df['Market value'].unique()[0]

                if len(str(Market)) == 6:
                        Market = str(Market)[:3]
                                
                elif len(str(Market)) == 7:
                        if str(Market)[:2][1] != 0:
                                Market = str(Market)[:2][0] + '.' + str(Market)[:2][1] + 'M'
                        
                elif len(str(Market)) == 8:
                        Market = str(Market)[:2] + 'M'

                elif len(str(Market)) == 9:
                        Market = str(Market)[:3] + 'M'
                
                elif Market == 0:
                        Market = 'Unknown data'
                
                Market = str(Market)

                position = df['Position'].unique()[0]
                if ', ' in position:
                        position = position.split(', ')[0]

                Contract = df['Contract expires'].unique()[0]

                Height = df['Height'].unique()[0]

                Foot = df['Foot'].unique()[0]

                mainPos = df['Main Pos'].unique()[0]

                age = df['Age'].unique()[0]

                team = df['Team'].unique()[0]

                if role_Selected != None:
                        role = role_Selected
                else:
                        role = df['Role'].unique()[0]
                print('Role em campo: ', role)

                #######################################################################################################################################

                fig = plt.figure(figsize=(15, 10), dpi=1000, facecolor = background)
                ax = fig.subplots()
                gspec = gridspec.GridSpec(
                ncols=2, nrows=2, wspace = 0.5
                )

                ########################################################################################################################################################

                ax1 = plt.subplot(
                                gspec[0, 0],
                        )
                
                ax1.set_facecolor(background)
                ax1.axis('off')

                ax_text(x=1, y=2.3,  s=playerName, va='center', ha='center',
                        size=35, color=color, ax=ax1)

                profile = df['Player Profile'].explode().unique()[0]

                ax_text(x=0.25, y=0.4,  s='Perfil Jogador', va='center', ha='center',
                        size=18, color='#FCAC14', ax=ax1)
                
                ax_text(x=0.28, y=0.25,  s=profile, va='center', ha='center',
                        size=9, color=color, ax=ax1)
                
                fig = add_image(image='./Images/profile.png', fig=fig, left=0.113, bottom=0.6595, width=0.03, height=0.03)
                
                #######################################################################################################################################
                
                setPieces = df['SetPieces Profile'].explode().unique()[0]
                
                decision = df['KeyPass Profile'].explode().unique()[0]
                
                SightPlay = df['SightPlay Profile'].explode().unique()[0]
                
                OffBall = df['OffBall Profile'].explode().unique()[0]
                
                Pass = df['Pass Profile'].explode().unique()[0]
                
                Concentration = df['Concentration Profile'].explode().unique()[0]
                
                Touch = df['Touch Profile'].explode().unique()[0]
                
                Chances = df['Chances Profile'].explode().unique()[0]
                
                #dribbling = data['dribbling Profile'].explode().unique()[0]
                
                ax_text(x=1, y=2,  s='Com bola', va='center', ha='center',
                        size=18, color='#FCAC14', ax=ax1)

                ax_text(x=1.15, y=1.7,  s= SightPlay + '\n''\n' + Pass + '\n''\n' + Chances, va='center', ha='center',
                                           size=9, color=color, ax=ax1)
                
                fig = add_image(image='./Images/soccer-ball.png', fig=fig, left=0.374, bottom=1.22, width=0.024, height=0.024)

                #######################################################################################################################################
                        
                ax_text(x=1, y=1.28,  s='Sem bola', va='center', ha='center',
                        size=18, color='#FCAC14', ax=ax1)

                #ax_text(x=1, y=1.15,  s='• Jogador muito forte no ataque ao espaço\nmovimenta-se muito bem dentro do campo', va='center', ha='center',
                #        size=9, color=color, ax=ax1)
                
                fig = add_image(image='./Images/lupa.png', fig=fig, left=0.37, bottom=0.964, width=0.03, height=0.03)

                #######################################################################################################################################

                ax_text(x=1, y=0.9,  s='Perfil Fisico', va='center', ha='center',
                        size=18, color='#FCAC14', ax=ax1)

                #(x=1.15, y=0.7,  s='• Rápido na pressão ao portador da bola juntamente com o seu porte fisico\nconsegue recuperar várias vezes a posse.\n\n• Veloz com bola, boa agilidade consegue facilmente mudar de sentido,\ndemonstra fragildidade nos duelos de corpo como também nos duelos aéreos.', va='center', ha='center',
                #        size=9, color=color, ax=ax1)
                
                fig = add_image(image='./Images/user.png', fig=fig, left=0.36, bottom=0.82, width=0.032, height=0.05)

                #######################################################################################################################################

                values = []
                params = ['Habilidade Passe', 'Habilidade Passe Decisivo', 'Habilidade Bola Parada', 'Habilidade Drible',
                          'Visão de Jogo', 'Habilidade Criar Chances', 'Concentração', 'Habilidade Finalização', 'Habilidade Cabeceio',
                          'Habilidade Interceptação', 'Habilidade Desarme', 'Habilidade Aérea', 'Habilidade Defensiva']
                
                if role_Selected != None:
                        df2 = data2[(data2['Comp'] == league) & ((data2['Role'] == role_Selected) | (data2['Role2'] == role_Selected)) &
                            ((data2['Minutes played'] <= minutes) | (data2['Minutes played'] >= minutes_2))][params].reset_index(drop=True)
                else:
                        df2 = data2[(data2['Comp'] == league) & (data2['Main Pos'] == mainPos) &
                                ((data2['Minutes played'] <= minutes) | (data2['Minutes played'] >= minutes_2))][params].reset_index(drop=True)

                player = df[(df['Player'] == playerName) & (df['Team'] == team) &
                            (df['League'] == league_Player) & (df['Season'] == season)][params].reset_index(drop=True)
                
                player = list(player.loc[0])
                player = [value * number for value in player]
                #player = player[1:]

                #######################################################################################################################################

                for x in range(len(params)):
                        values.append(math.floor(stats.percentileofscore((df2[params[x]]), player[x])))

                for n, i in enumerate(values):
                        if i == 100:
                                values[n] = 99
                print(values)
                elite = []
                veryStrong = []
                strong = []
                improve = []
                weak = []
                veryWeak = []
                for i in range(len(values)):
                        if values[i] >= 95:
                                elite.append(params[i])

                        elif (values[i] >= 80) & (values[i] < 95):
                                veryStrong.append(params[i])

                        elif (values[i] >= 70) & (values[i] < 80):
                                strong.append(params[i])

                        elif (values[i] >= 40) & (values[i] < 70):
                                improve.append(params[i])

                        elif (values[i] < 40) & (values[i] >= 25):
                                weak.append(params[i])

                        elif values[i] < 25:
                                veryWeak.append(params[i])
                        
                #######################################################################################################################################
                
                highlight_textpropsElite =\
                [{"color": '#2ae102', "fontweight": 'bold'}]

                highlight_textpropsVeryStrong =\
                [{"color": '#2cb812', "fontweight": 'bold'}]
                
                highlight_textpropsStrong =\
                [{"color": '#2a9017', "fontweight": 'bold'}]

                highlight_textpropsImprovment =\
                [{"color": '#f48515', "fontweight": 'bold'}]

                ax_text(x=2, y=2, s='<Pontos fortes>', va='center', ha='center',
                                        highlight_textprops = highlight_textpropsElite, size=18, color=color, ax=ax1)

                h=1.95
                for i in elite:
                        ax_text(x=2, y=h - 0.07, s='<Elite:>' + ' ' + i, va='center', ha='center',
                                highlight_textprops = highlight_textpropsElite, size=11, color=color, ax=ax1)
                        h=h-0.07

                h=h
                for i in veryStrong:
                        ax_text(x=2, y=h - 0.07, s='<Muito forte:>' + ' ' + i, va='center', ha='center',
                                highlight_textprops = highlight_textpropsVeryStrong, size=11, color=color, ax=ax1)
                        h=h-0.07

                h=h
                for i in strong:
                        ax_text(x=2, y=h - 0.07, s='<Forte:>' + ' ' + i, va='center', ha='center',
                                highlight_textprops = highlight_textpropsStrong, size=11, color=color, ax=ax1)
                        h=h-0.07

                ax_text(x=2, y=h - 0.25, s='<Pontos a melhorar>', va='center', ha='center',
                                        highlight_textprops = highlight_textpropsImprovment, size=18, color=color, ax=ax1)

                h=h - 0.3
                for i in improve:
                        ax_text(x=2, y=h - 0.07, s='<Melhorar:>' + ' ' + i, va='center', ha='center',
                                highlight_textprops = highlight_textpropsImprovment, size=11, color=color, ax=ax1)
                        h=h-0.07

                h=h
                for i in weak:
                        ax_text(x=2, y=h - 0.07, s='<Melhorar:>' + ' ' + i, va='center', ha='center',
                                highlight_textprops = highlight_textpropsImprovment, size=11, color=color, ax=ax1)
                        h=h-0.07

                h=h
                for i in veryWeak:
                        ax_text(x=2, y=h - 0.07, s='<Melhorar:>' + ' ' + i, va='center', ha='center',
                                highlight_textprops = highlight_textpropsImprovment, size=11, color=color, ax=ax1)
                        h=h-0.07


                highlight_textpropsInfo =\
                [{"color": '#FCAC14', "fontweight": 'bold'}]

                #######################################################################################################################################

                ax_text(x=0.04, y=1.7,  s='<Idade:> ' + str(age), va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1.6,  s='<Equipe:> ' + team, va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1.5,  s='<Altura:> ' + str(Height) + ' cm', va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1.4,  s='<Contrato:> ' + Contract, va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1.3,  s='<Valor:> ' + Market, va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1.2,  s='<Pé:> ' + Foot, va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1.1,  s='<Posição:> ' + mainPos, va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)

                #######################################################################################################################################

                ax_text(x=0.04, y=1,  s='<Função:> ' + role, va='center', ha='center',
                        size=14, highlight_textprops = highlight_textpropsInfo, color=color, ax=ax1)
                
                #######################################################################################################################################

                highlight_textpropsNotBest =\
                [{"color": '#FF0000', "fontweight": 'bold'}]

                highlight_textprops_To_Improvment =\
                [{"color": '#ffdb0a', "fontweight": 'bold'}]
 
                print('Posição: ', mainPos)
                bestRole = df['Role'].values[0]
                print('\nRole Jogador: ', bestRole)
                if role_Selected:
                        roleValue = round(df[role_Selected], 2)
                else:
                        roleValue = round(df[score_column], 2)
                roleValue = roleValue * number
                print('\nScore Jogador: ', roleValue)

                df2 = data2[(data2['Comp'] == league) & (data2['Main Pos'] == mainPos) &
                            ((data2['Minutes played'] <= minutes) | (data2['Minutes played'] >= minutes_2))].reset_index(drop=True)
                print(f'\n{league}: ', df2[bestRole].values)

                if role_Selected:

                        df2 = data2[(data2['Comp'] == league) & ((data2['Role'] == role_Selected) | (data2['Role2'] == role_Selected)) &
                                ((data2['Minutes played'] <= minutes) | (data2['Minutes played'] >= minutes_2))].reset_index(drop=True)
                        scores = df2[role_Selected].values
                        print(f'\n{league}: ', scores)
                else:
                        pass
                
                scores = df2[bestRole].values

                rolePercentile = math.floor(stats.percentileofscore(scores, roleValue))
                print('\nPercentile Jogador: ', rolePercentile)

                if rolePercentile >= 90:
                        ax_text(x=1.2, y=0.39,  s='NOTA',
                                va='center', ha='center', size=28,
                                color=color, ax=ax1)
                
                        ax_text(x=1.213, y=0.24,  s='<A>',
                                va='center', ha='center', size=40,
                                highlight_textprops = highlight_textpropsElite, color=color, ax=ax1)
                
                elif (rolePercentile < 90) & (rolePercentile >= 75):
                        ax_text(x=1.2, y=0.39,  s='NOTA',
                                va='center', ha='center', size=28,
                                color=color, ax=ax1)
                
                        ax_text(x=1.213, y=0.24,  s='<B>',
                                va='center', ha='center', size=35,
                                highlight_textprops = highlight_textpropsStrong, color=color, ax=ax1)

                elif (rolePercentile < 75) & (rolePercentile >= 60):
                        ax_text(x=1.2, y=0.39,  s='NOTA',
                                va='center', ha='center', size=28,
                                color=color, ax=ax1)
                
                        ax_text(x=1.213, y=0.24,  s='<C>',
                                va='center', ha='center', size=35,
                                highlight_textprops = highlight_textprops_To_Improvment, color=color, ax=ax1)

                elif (rolePercentile < 60) & (rolePercentile >= 40):
                        ax_text(x=1.2, y=0.39,  s='NOTA',
                                va='center', ha='center', size=28,
                                color=color, ax=ax1)
                
                        ax_text(x=1.213, y=0.24,  s='<D>',
                                va='center', ha='center', size=35,
                                highlight_textprops = highlight_textpropsImprovment, color=color, ax=ax1)

                elif (rolePercentile < 40) & (rolePercentile >= 0):
                        ax_text(x=1.2, y=0.39,  s='NOTA',
                                va='center', ha='center', size=28,
                                color=color, ax=ax1)
                
                        ax_text(x=1.213, y=0.24,  s='<E>',
                                va='center', ha='center', size=35,
                                highlight_textprops = highlight_textpropsNotBest, color=color, ax=ax1)

                ax_text(x=1.213, y=0.11,  s=f'{str(rolePercentile / 10)}/10',
                                va='center', ha='center', size=25,
                                color=color, ax=ax1)
                
                #######################################################################################################################################

                import datetime

                current_datetime = datetime.datetime.now()
                today = current_datetime.date()

                ax_text(x=1.5, y=0.39,  s='DATA',
                        va='center', ha='center', size=28,
                        color=color, ax=ax1)

                ax_text(x=1.5, y=0.24,  s=str(today),
                        va='center', ha='center', size=14,
                        color=color, ax=ax1)

                #######################################################################################################################################

                fig_Player = add_image(image=f'Images/player_Icon.png', fig=fig, left=0.1, bottom=1.17, width=0.11, height=0.14)
                fig = add_image(image='./Images/Country/' + country + '.png', fig=fig, left=0.185, bottom=1.2, width=0.07, height=0.06)
                fig_DIMAS = add_image(image='./Images/DIMAS - Extenso - Fundo transparente.png', fig=fig, left=0.73, bottom=1.3, width=0.14, height=0.14)

                # Ensure the 'Images' folder exists
                if not os.path.exists(f'Images/Recruitment/{playerName}'):
                        os.makedirs(f'Images/Recruitment/{playerName}')

                # Adjust the layout
                plt.tight_layout()

                # Save the figure
                plt.savefig(f'Images/Recruitment/{playerName}/{playerName} Report.png', bbox_inches='tight', dpi=300)

                return plt.show()

        return report(playerName, league, team, league_Player)

with st.form("select-buttons"):

        options_Player = st.sidebar.selectbox(
        'Choose Player you want analyse',
        sorted(wyscout.Player.unique()))

        options_Team = st.sidebar.selectbox(
                'Select the players team',
                sorted(wyscout[wyscout['Player'] == options_Player]['Team'].unique()))

        options_League = st.sidebar.selectbox(
                'Select the players league',
                sorted(wyscout[wyscout['Player'] == options_Player]['League'].unique()))

        leagues_List = wyscout.Comp.unique().tolist()
        leagues_List.insert(0, 'Player League')

        league_Context = st.sidebar.selectbox(
        'Choose league you want analyse', leagues_List)

        if league_Context == 'Player League':
                league = wyscout.loc[wyscout['Player'] == options_Player]['Comp'].unique()[0]
        else:
                league = league_Context

        Season_List = wyscout.loc[(wyscout['Team'] == options_Team) & (wyscout['League'] == options_League) &
                                  (wyscout['Player'] == options_Player)]['Season'].unique()

        Season = st.sidebar.selectbox(
        'Choose Season you want analyse', Season_List)

        role_Choice = st.sidebar.selectbox(
                        'You want to select a role?', ['No', 'Yes'])
        
        if role_Choice == 'Yes':
                roles_List = st.sidebar.selectbox(
                        'You want to select a role?', wyscout['Role'].unique())
        else:
                roles_List = None

        score_Adjusted = st.sidebar.selectbox(
                        'Has the score been already adjusted?', ['No', 'Yes'])

        if score_Adjusted == 'No':
                number_Adjust = st.sidebar.selectbox(
                        'Choose value to adjust the player scores', [1, 0.95, 0.93, 0.90, 0.88, 0.85, 0.82, 0.80, 0.78, 0.75])
                score_column = 'Score'
        else:
                number_Adjust = 1
                score_column = 'AdjustedScore'

        minutes_Lower = st.sidebar.selectbox(
        'Set minimum minutes', list(range(0, 30000)))

        minutes_Max = st.sidebar.selectbox(
        'Set maximium minutes', list(range(0, 30000)))

        btn1 = st.form_submit_button(label='Player Report')

#col1, col2, col3, col4, col5, col6 = st.columns(6)

if btn1:
        figTraditionReport = traditionalReport(wyscout, league, options_Player, options_Team, options_League, Season, score_column, number_Adjust, minutes_Lower, minutes_Max, roles_List)

        st.text('This is a test version to combine the data report (strengths and to improve) with the traditional scout report with tactical aspects of the player (On and Off ball momentum and physical).')

        st.text("Note that the value at the moment 'On Ball' are predefined values and have nothing to do with the player.")

        st.pyplot(figTraditionReport)