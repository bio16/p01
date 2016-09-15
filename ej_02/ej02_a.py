#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Uso la librería igraph y pandas.
import igraph
import pandas as pd

# ------- Cargo la informacion del problema ------------- #

# Cargo en el objeto graph la red de dolphins.gml.
graph = igraph.read('dolphins.gml')

# Leo la info sobre el sexo de los delfines.
dolphins_sex = pd.read_table('dolphinsGender.txt', header = None)    

# Le asigno a cada vértice la información sobre el nombre
# y el sexo, reflejado en el color del vertice en el plot.
# Nodo Azul: macho.
# Nodo Rosa: hembra.
# Nodo Verde: sexo desconocido.
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

# ------ Distintos layouts - parte a ------------------- #
#----- Generamos los distinos layouts ------------------ #

# Layouts que nos dan una buena visualización

# Grafo Fruchterman - Reingold
layout = graph.layout_fruchterman_reingold()
igraph.plot(graph, layout = layout, target = 'FrutRein.eps')

# Grafo Kamada Kawai
layout = graph.layout_kamada_kawai()
igraph.plot(graph, layout = layout, target = 'KamKaw.eps')

# Grafo DrL
layout = graph.layout_drl()
igraph.plot(graph, layout = layout, target = 'Drl.eps')

# Layouts que NO nos da una buena visualización

# Grafo Random
layout = graph.layout_random()
igraph.plot(graph, layout = layout, target = 'Random.eps')

# Grafo Multidimensional Scaling
layout = graph.layout_mds()
igraph.plot(graph, layout = layout, target = 'Multi.eps')
