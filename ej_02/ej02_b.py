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

# ----- Parte b ------ #

# Cuento la cantidad de especies del mismo género
number_of_vertices = len(graph.vs)
print number_of_vertices

number_of_links = len(graph.es)

genders = {}
genders['f'] = 0
genders['m'] = 0
genders[None] = 0
for vs in graph.vs:
    genders[vs['sex']] += 1

print u'Fracción de delfines machos:' + str(float(genders['m'])/number_of_vertices)
print u'Fracción de delfines hembras:' + str(float(genders['f'])/number_of_vertices)
print u'Fracción de delfines con género no especificado:' + str(float(genders[None])/number_of_vertices)

# Calculo la cantidad de links entre géneros que existen
# No tomo en cuenta links con los delfines de género indefinido
inter_gender_links = 0
for vs in graph.vs:
    neighbors = vs.neighbors()
    for neighbour in neighbors:
        if vs['sex'] != neighbour['sex'] and \
           vs['sex'] != None and neighbour['sex'] != None: 
            inter_gender_links += 1

# Real gender links son los links entre géneros de la red del dataset
real_gender_links = inter_gender_links / 2

print u'Fracción de enlaces entre géneros: ' + str(float(real_gender_links)/number_of_links)


# Paso a sortear los géneros entre los vértices manteniendo
# la topología de la red inalterable. 
# De cada sorteo calculo el número de links entre especies
# de distinto género y devuelvo el histograma.

list_of_genders = ['m'] * genders['m'] + ['f'] * genders['f'] + \
                  [None] * genders[None]

# Fracción de links entre generos 
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


    aux = inter_gender_links / 2
    inter_gender_links_data.append(aux)

# Imprimo el valor medio y la desviación standard 
# de la distribución resultante
print u'Valor medio y desviación de la distribución: '
print np.mean(inter_gender_links_data)/number_of_links,
print np.std(inter_gender_links_data)/number_of_links

plt.figure(1)
plt.hist(inter_gender_links_data, range = [40.5, 90.5], bins = 50, normed = True, label = u'Distribución nula')
plt.plot([real_gender_links, real_gender_links], [0.0, 0.01], '.-', markersize = 15, label = 'Red real')
plt.legend(loc = 2)
plt.xlabel(u'# de Links entre géneros')
plt.xlim([40, 90])

plt.grid('on')
plt.title(u'Número total de links = ' + str(number_of_links))

plt.savefig('Histograma.eps')

plt.yscale('log')
plt.savefig('Histograma_log.eps')
