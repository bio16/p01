#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Uso la librería igraph y pandas.
import igraph
import pandas as pd
import random as rand
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

# ---- Parte c ---- #

from copy import deepcopy

graph_aux = deepcopy(graph)

# Número de nodos a remover
# Remuevo los nodos desde mayor betweennes
# Al remover 4 vertices con este algoritmo
# se logra particionar la red en dos comunas
# de tamaño comparable.

nodes_to_remove = 50
size_max_component = np.zeros(nodes_to_remove)

j = 0

for i in range(nodes_to_remove):
    # Calculo el betweenness
    betweenness = graph_aux.betweenness()
    # Elijo el max
    max_bet = max(betweenness)
    vertex_ind = betweenness.index(max_bet)

    # Remuevo el vertice
    graph_aux.delete_vertices(vertex_ind)

    # Imprimo el layout
    layout = graph_aux.layout_fruchterman_reingold()
    if i < 4:
        igraph.plot(graph_aux, layout = layout, target = 'Parte_c' + str(i) + '.eps')
    graph_aux2 = graph_aux.clusters()
    size_max_component[j] +=  max(graph_aux2.sizes())
    j += 1

plt.plot(range(nodes_to_remove), size_max_component, '.-', markersize = 10, label = 'Por betweenness')

size_max_component = np.zeros(nodes_to_remove)

for conf in range(1000):

    graph_aux = deepcopy(graph)

    j = 0

    for i in range(nodes_to_remove):

        vertex2remove = rand.randint(0, len(graph_aux.vs) - 1)
        # Remuevo el vertice
        graph_aux.delete_vertices(vertex2remove)

        graph_aux2 = graph_aux.clusters()
        size_max_component[j] +=  max(graph_aux2.sizes())
 
        j += 1

size_max_component = size_max_component / 1000

plt.plot(range(nodes_to_remove), size_max_component, '.-', markersize = 10, label = 'Por azar')
plt.legend()
plt.grid('on')
plt.xlabel(u'Número de nodos removidos')
plt.ylabel(u'Tamaño del componente más grande')
plt.savefig('Nodos_removidos.eps')
