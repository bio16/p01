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

# --------------------- Parte c --------------------- #

from copy import deepcopy

# Creo una copia del grafo en un objeto auxiliar
graph_aux = deepcopy(graph)

# Número de nodos a remover

# Comienzo a remover nodos con mayor betweenness.
# Con solo remover cuatro nodos ya se logra separar
# la red en dos componentes de tamaño comparable.
# Calculo luego de cada remoción, el tamaño del
# componente (nodos conectados) más grande del sistema.

# Nodos a remover
nodes_to_remove = 50

j = 0
size_max_component = np.zeros(nodes_to_remove)
for i in range(nodes_to_remove):

    # Calculo el betweenness
    betweenness = graph_aux.betweenness()

    # Elijo el nodo con mayor betweenness
    max_bet = max(betweenness)
    vertex_ind = betweenness.index(max_bet)

    # Remuevo el vertice
    graph_aux.delete_vertices(vertex_ind)

    # Imprimo el layout solo hasta la cuarta remoción 
    # (allí la red ya se particiona en dos)
    layout = graph_aux.layout_fruchterman_reingold()
    if i < 4:
        igraph.plot(graph_aux, layout = layout, target = 'Parte_c' + str(i) + '.eps')

    # Calculo y guardo el tamaño de la componente más grande
    graph_aux2 = graph_aux.clusters()
    size_max_component[j] +=  max(graph_aux2.sizes())
    j += 1

# Grafico el tamaño de la componente más grande en función de la 
# cantidad de nodos removidos.
plt.plot(range(nodes_to_remove), size_max_component, '.-', markersize = 10, label = 'Por betweenness')

# Realizo el mismo procedimiento, pero removiendo nodos al azar.
# Luego calculo el promedio de 1000 realizaciones del tamaño 
# del componente más grande en función de los nodos removidos.
size_max_component = np.zeros(nodes_to_remove)
for conf in range(1000):

    j = 0
    graph_aux = deepcopy(graph) 

    for i in range(nodes_to_remove):

	# Elijo un nodo al azar
        vertex2remove = rand.randint(0, len(graph_aux.vs) - 1)
        
        # Remuevo el nodo
        graph_aux.delete_vertices(vertex2remove)

        # Calculo el tamaño del componente más grande
        graph_aux2 = graph_aux.clusters()
        size_max_component[j] +=  max(graph_aux2.sizes()) 
        j += 1

# Calculo el promedio de todas las realizaciones
size_max_component = size_max_component / 1000

# Grafico la evolución del tamaño del componente más grande en 
# función de la cantidad de nodos removidos al azar.
plt.plot(range(nodes_to_remove), size_max_component, '.-', markersize = 10, label = 'Por azar')

plt.legend()
plt.grid('on')
plt.xlabel(u'Número de nodos removidos')
plt.ylabel(u'Tamaño del componente más grande')
plt.savefig('Nodos_removidos.eps')
