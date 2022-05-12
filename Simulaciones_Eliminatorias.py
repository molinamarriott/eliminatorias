# -*- coding: utf-8 -*-
"""
After the victory of Ecuador in Santiago I propose estimate the probability of qualifying
with 3 games to play. I do this exercise simulating 5000 times the remaining games. 
The results gives Ecuador around 99.8% of qualifying. The output of this code is a 
boxplots chart of the points estimated by each national team and a gif with the evolution 
of  the simulations.

"""

import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import imageio
import os

def tabla(dicc):
    paises = dicc.keys()
    pjs,puntos,fav,con,ganados,perdidos= [],[],[],[],[],[]
    for pais in paises:
        pjs.append(dicc[pais][0])
        ganados.append(dicc[pais][1])
        perdidos.append(dicc[pais][3])
        fav.append(dicc[pais][4])
        con.append(dicc[pais][5])
        puntos.append(dicc[pais][6])
    df = pd.DataFrame(list(zip(pjs,ganados,perdidos,fav,con,puntos)),
               columns =['P.Jugados', 'P.Ganados', "P.Perdidos", "G.favor",
                         "G.Contra", "Puntos"])
    df.insert(2, "P.Empatados", df["P.Jugados"]-df["P.Ganados"]-df["P.Perdidos"],
              True)
    df.insert(6, "Dif.Goles", df["G.favor"]-df["G.Contra"],
              True)
    df.insert(0, "Seleccion",paises,True)
    df = df.sort_values(['Puntos', 'Dif.Goles'],ascending=False)
    df.insert(9,"Index",range(1,11))
    df = df.set_index(["Index"])
    return df


def partido(matchs):
    resultado = random.randint(0,len(matchs)-1)
    score = matchs[resultado]
    return score
    
def asignacion(local,visitante,gol_local,gol_visitante,dicc):
    dicc[local][-3] += gol_local
    dicc[visitante][-3] += gol_visitante
    dicc[local][-2] += gol_visitante
    dicc[visitante][-2] += gol_local
    if gol_local == gol_visitante:
        dicc[local][0] += 1
        dicc[local][2] += 1
        dicc[local][-1] += 1
        dicc[visitante][0] += 1
        dicc[visitante][2] += 1
        dicc[visitante][-1] += 1
    if gol_local > gol_visitante:
        dicc[local][0] += 1
        dicc[local][1] += 1
        dicc[local][-1] += 3
        dicc[visitante][0] += 1
        dicc[visitante][3] += 1
        dicc[visitante][-1] += 0
    if gol_local < gol_visitante:
        dicc[visitante][0] += 1
        dicc[visitante][1] += 1
        dicc[visitante][-1] += 3
        dicc[local][0] += 1
        dicc[local][3] += 1
        dicc[local][-1] += 0
    return dicc

def simulacion(dicc,fechas,fixtures):
    for fecha in fechas:
        local = fecha[0]
        visitante = fecha[1]
        g_loc, g_visit = partido(fixtures)
        asignacion(local, visitante, g_loc, g_visit, dicc)
    return dicc

def iteraciones(n,fechas,fixtures):
    resul={}
    for i in range(1,n):
        dicc1 = {"Brasil": [13,11,2,0,27,4,35],
                   "Argentina": [13,8,5,0,20,6,29],
                   "Ecuador": [14,7,2,5,23,13,23],
                   "Colombia":[14,3,8,3,16,17,17],
                   "Peru":[14,5,2,7,15,20,17],
                   "Chile":[14,4,4,6,15,16,16],
                   "Uruguay":[14,4,4,6,14,21,16],
                   "Bolivia":[14,4,3,7,20,28,15],
                   "Paraguay":[14,2,7,5,9,18,13],
                   "Venezuela":[14,2,1,11,9,25,7]}
        sim = simulacion(dicc1, fechas, fixtures)
        df = tabla(sim)
        for index, row in df.iterrows():
            pais = row["Seleccion"]
            if not (pais in resul.keys()):
                resul[pais] = [index]
            else:
                resul[pais].append(index)
        del sim, df, pais, index, dicc1
    return resul


def iteraciones_2(n,fechas,fixtures):
    resul={}
    for i in range(1,n):
        dicc1 = {"Brasil": [13,11,2,0,27,4,35],
                   "Argentina": [13,8,5,0,20,6,29],
                   "Ecuador": [14,7,2,5,23,13,23],
                   "Colombia":[14,3,8,3,16,17,17],
                   "Peru":[14,5,2,7,15,20,17],
                   "Chile":[14,4,4,6,15,16,16],
                   "Uruguay":[14,4,4,6,14,21,16],
                   "Bolivia":[14,4,3,7,20,28,15],
                   "Paraguay":[14,2,7,5,9,18,13],
                   "Venezuela":[14,2,1,11,9,25,7]}
        sim = simulacion(dicc1, fechas, fixtures)
        df = tabla(sim)
        for index, row in df.iterrows():
            pais = row["Seleccion"]
            if not (pais in resul.keys()):
                resul[pais] = [row["Puntos"]]
            else:
                resul[pais].append(row["Puntos"])
        del sim, df, pais, index, dicc1
    return resul
        
        

    

puntaje = {"Brasil": [13,11,2,0,27,4,35],
           "Argentina": [13,8,5,0,20,6,29],
           "Ecuador": [14,7,2,5,23,13,23],
           "Colombia":[14,3,8,3,16,17,17],
           "Peru":[14,5,2,7,15,20,17],
           "Chile":[14,4,4,6,15,16,16],
           "Uruguay":[14,4,4,6,14,21,16],
           "Bolivia":[14,4,3,7,20,28,15],
           "Paraguay":[14,2,7,5,9,18,13],
           "Venezuela":[14,2,1,11,9,25,7]}

puntaje = dict(puntaje)  


partidos = [("Ecuador","Brasil"),("Paraguay","Uruguay"),("Chile","Argentina"),
            ("Colombia","Peru"),("Venezuela","Bolivia"), # Siguiente Fecha
            ("Bolivia","Chile"),("Uruguay","Venezuela"),("Argentina","Colombia"),
            ("Brasil","Paraguay"),("Peru","Ecuador"), #Siguiente Fecha
            ("Argentina","Venezuela"),("Colombia","Bolivia"),("Paraguay","Ecuador"),
            ("Brasil","Chile"),("Uruguay","Peru"), #Siguiente Fecha
            ("Peru","Paraguay"),("Ecuador","Argentina"),("Venezuela","Colombia"),
            ("Chile","Uruguay"),("Bolivia","Brasil"), #Por ultimo
            ("Brasil","Argentina")]

resultados = [(2,2),(2,1),(1,0),(3,0),(5,0),(1,2),(4,2),
              (0,1),(2,4),(2,2),(2,3),(1,1),(0,3),(2,0),
              (1,0),(6,1),(2,1),(2,2),(0,2),(0,2),(3,1),
              (0,0),(1,1),(0,3),(2,0),(1,2),(0,0),(2,2),
              (0,2),(1,1),(1,1),(2,0),(1,3),(1,1),(0,1),
              (0,0),(4,2),(4,2),(1,1),(1,0),(1,0),(2,1),
              (3,1),(3,0),(2,0),(0,0),(0,0),(1,3),(3,0),
              (2,0),(1,0),(2,1),(0,0),(0,3),(2,0),(4,0),
              (0,0),(1,0),(3,0),(4,1),(1,0),(0,1),(1,0),
              (3,0),(0,1),(3,0),(1,2),(0,0),(0,0),(0,2)]

w = iteraciones(5001,partidos,resultados)

df = pd.DataFrame(data=w, index=range(1,5001))

df["clasifica_ecu"] = np.where(df['Ecuador']<5, 1,0)
df["Simulacion"] = range(1,5001)
df["SumaCasos"]=df["clasifica_ecu"].cumsum()
df["Probabilidades"]=df["SumaCasos"]/df["Simulacion"]

df["repechaje_ecu"] = np.where(df['Ecuador']==5, 1,0)
df["Casos_Repechaje"]=df["repechaje_ecu"].cumsum()
df["Probabilidades_2"]=df["Casos_Repechaje"]/df["Simulacion"]

df["eliminacion_ecu"] = np.where(df['Ecuador']>5, 1,0)
df["Casos_Eli"]=df["eliminacion_ecu"].cumsum()
df["Probabilidades_3"]=df["Casos_Eli"]/df["Simulacion"]



##### Grafica conjunta


fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(df["Simulacion"], df["Probabilidades"]*100,color="black")
ax1.hlines(y=df["Probabilidades"].iloc[-1]*100, xmin=1, xmax=5000, linewidth=1, color='r')
ax1.set_title('Probabilidad de clasificación directa')
ax2.plot(df["Simulacion"], df["Probabilidades_2"]*100,color="black")
ax2.hlines(y=df["Probabilidades_2"].iloc[-1]*100, xmin=1, xmax=5000, linewidth=1, color='r')
ax2.set_title('Probabilidad de repechaje')
ax3.plot(df["Simulacion"], df["Probabilidades_3"]*100,color="black")
ax3.hlines(y=df["Probabilidades_3"].iloc[-1]*100, xmin=1, xmax=5000, linewidth=1, color='r')
ax3.set_title('Probabilidad de Eliminación')
fmt = "%.02f" # Format you want the ticks, e.g. '40%'
xticks = mtick.PercentFormatter(decimals=2)
ax1.yaxis.set_major_formatter(xticks)
ax2.yaxis.set_major_formatter(xticks)
ax3.yaxis.set_major_formatter(xticks)
fig.tight_layout()
fig.savefig('full_figure.png',dpi=200)


### Grafica animada


y=[500,1000,1500,2000,2500,3000,3500,4000,4500,5000]

filenames = []
for i in y:
    # plot the line chart
    plt.plot(df["Simulacion"].iloc[:i],df["Probabilidades"].iloc[:i]*100,
             color="black")
    plt.title("Probabilidad de clasificación directa")
    plt.xlabel('Simulaciones')
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename)
    plt.close()
# build gif
with imageio.get_writer('mygif.gif', mode='I', duration=1) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        
# Remove files
for filename in set(filenames):
    os.remove(filename)


#___________________________________________________________________________


w2 = iteraciones_2(5001,partidos,resultados)

w2 = pd.DataFrame(w2).melt()



import seaborn as sns

grouped = w2.loc[:,['variable', 'value']].groupby(['variable']).median().sort_values(by='value')

colors = ["#ccff66", "#00ffff","#ffff00","#ffffff","#ffff66","#99ccff",
          "#ff0000","#009900","#ff8080","#ac3939"]

sns.set(style='whitegrid')
sns.set_palette(sns.color_palette(colors))
sns.boxplot(y='variable', x='value', data=w2, order=grouped.index[::-1])
plt.xticks(rotation=90)
plt.ylabel('')
plt.xlabel('Puntos al final de la eliminatoria')
plt.savefig('tabla.png',dpi=250, transparent=False, bbox_inches='tight')
