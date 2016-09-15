#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Uso la librería igraph y pandas.
import igraph
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

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

"""
# ------ Distintos layouts - parte a ------------------- #

# Grafo circular
layout = graph.layout_circle()
igraph.plot(graph, layout = layout, target = 'Circle.eps')

# Grafo DrL
layout = graph.layout_drl()
igraph.plot(graph, layout = layout, target = 'Drl.eps')

# Grafo Fruchterman - Reingold
layout = graph.layout_fruchterman_reingold()
igraph.plot(graph, layout = layout)

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

# ----- Parte b ------ #

# Cuento la cantidad de especies del mismo género

number_of_vertices = len(graph.vs)
number_of_links = len(graph.es)

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

print u'Fracción de enlaces entre géneros: ' + str(float(real_gender_links) / number_of_links)

print u'Fracción de enlaces entre géneros según hipótesis nula: ' + str(2.0 * genders['m'] * genders['f'] / (number_of_vertices * number_of_vertices))

# Paso a sortear los géneros entre los vértices manteniendo
# la topología de la red inalterable. 
# De cada sorteo calculo el número de links entre especies
# de distinto género y devuelvo el histograma.

list_of_genders = ['m'] * genders['m'] + ['f'] * genders['f'] + \
                  [None] * genders[None]

inter_gender_links_data = []

for conf in range(1000000):

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

print u'Valor medio y desviación de la distribución: '
print np.mean(inter_gender_links_data)/number_of_links,
print np.std(inter_gender_links_data)/number_of_links


plt.ion()
plt.hist(inter_gender_links_data, range = [39.5, 89.5], bins = 50, normed = True, label = u'Distribución nula')
plt.plot([real_gender_links, real_gender_links], [0.0, 0.05], '.-', markersize = 15, label = 'Red real')
plt.legend(loc = 2)
plt.xlabel(u'# de Links entre géneros')

plt.grid('on')
plt.savefig('Histrograma_b.eps')
plt.yscale('log')
plt.savefig('Histrograma_b_log.eps')
plt.show()

"""
# ---- Parte c ---- #

# Número de nodos a remover
# Remuevo los nodos desde mayor betweennes
# Con cuatro alcanza
nodes_to_remove = 4 
for i in range(nodes_to_remove):
    betweenness = graph.betweenness()
    max_bet = max(betweenness)
    vertex_ind = betweenness.index(max_bet)
    graph.delete_vertices(vertex_ind)

# Grafo Fruchterman - Reingold
layout = graph.layout_fruchterman_reingold()
igraph.plot(graph, layout = layout, target = 'Parte_c.eps')


# Remuevo al azar: habría que ver como detectar que
# particionó la red
nodes_to_remove = 15
sample = random.sample(range(len(graph.vs)), nodes_to_remove)
graph.delete_vertices(sample)
"""