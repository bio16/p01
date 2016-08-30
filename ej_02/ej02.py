#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Uso la librería igraph y pandas.
import igraph
import pandas as pd
import random
import matplotlib.pyplot as plt

# ------- Cargo la informacion del problema ------------- #

# Cargo en el objeto graph la red de dolphins.gml.
graph = igraph.read('dolphins.gml')

# Leo la info sobre el sexo de los delfines.
dolphins_sex = pd.read_table('dolphinsGender.txt', header = None)    

# Le asigno a cada vértice la información sobre el nombre
# y el sexo, reflejado en el color del vertice en el plot.
# Verde es sexo desconocido.
color_dict = {'m': "blue", 'f': "pink"}
for i in range(len(dolphins_sex)):
    dolphin_name = dolphins_sex[0][i]
    dolphin_sex = dolphins_sex[1][i]
    for vs in graph.vs:
        if vs['label'] == dolphin_name:
            vs['name'] = dolphin_name
            vs['sex'] = dolphin_sex
            try:
                vs["color"] = color_dict[vs['sex']]
            except:
                vs["color"] = "green"
                vs["sex"] = None

# Cuento la cantidad de especies del mismo género
genders = {}
genders['f'] = 0
genders['m'] = 0
genders[None] = 0
for vs in graph.vs:
    genders[vs['sex']] += 1

# Calculo la cantidad de links entre géneros que existen
inter_gender_links = 0
for vs in graph.vs:
    neighbors = vs.neighbors()
    for neighbour in neighbors:
        if vs['sex'] != neighbour['sex'] and \
           vs['sex'] != None and neighbour['sex'] != None: 
            inter_gender_links += 1

# Real gender links es los links entre géneros de la red real
real_gender_links = inter_gender_links / 2



# Paso a sortear los géneros entre los vértices manteniendo
# la topología de la red inalterable. 
# De cada sorteo calculo el número de links entre especies
# de distinto género y devuelvo el histograma.

list_of_genders = ['m'] * genders['m'] + ['f'] * genders['f'] + \
                  [None] * genders[None]

inter_gender_links_data = []

for conf in range(10000):

    random.shuffle(list_of_genders)
    i = 0
    for vs in graph.vs:
        vs['sex'] = list_of_genders[i]
        i += 1

    inter_gender_links = 0
    for vs in graph.vs:
        neighbors = vs.neighbors()
        for neighbour in neighbors:
            if vs['sex'] != neighbour['sex'] and \
              vs['sex'] != None and neighbour['sex'] != None: 
                inter_gender_links += 1

    inter_gender_links_data.append(inter_gender_links / 2)

plt.hist(inter_gender_links_data, range = [40, 90], bins = 50, normed = True, label = u'Distribución nula')
plt.plot([real_gender_links, real_gender_links], [0.0, 0.05], '.-', markersize = 15, label = 'Red real')
plt.legend(loc = 2)
plt.xlabel('# de Links')
plt.savefig('Histrograma_b.eps')
plt.show()







"""
# -------------- Distintos layouts ------------------- #

# Grafo circular
layout = graph.layout_circle()
igraph.plot(graph, layout = layout, target = 'Circle.eps')

# Grafo DrL
layout = graph.layout_drl()
igraph.plot(graph, layout = layout, target = 'Drl.eps')

# Grafo Fruchterman - Reingold
layout = graph.layout_fruchterman_reingold()
igraph.plot(graph, layout = layout, target = 'FrutRein.eps')

# Grafo Kamada Kawai
layout = graph.layout_kamada_kawai()
igraph.plot(graph, layout = layout, target = 'KamKaw.eps')

# Grafo Large Graph Layout
layout = graph.layout_lgl()
igraph.plot(graph, layout = layout, target = 'Large.eps')

# Grafo Multidimensional Scaling
layout = graph.layout_mds()
igraph.plot(graph, layout = layout, target = 'Multi.eps')

# Grafo Random
layout = graph.layout_random()
igraph.plot(graph, layout = layout, target = 'Random.eps')

# Grafo Reingold Tilford
layout = graph.layout_reingold_tilford()
igraph.plot(graph, layout = layout, target = 'ReinTil.eps')

# Grafo Star
layout = graph.layout_star()
igraph.plot(graph, layout = layout, target = 'Star.eps')

# --------------------------------------------------- #
"""


