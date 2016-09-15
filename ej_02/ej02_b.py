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

# ------------------- Parte b ------------------------- #

# Numero de vértices y número de links totales en la red
number_of_vertices = len(graph.vs)
number_of_links = len(graph.es)

# Cargo en el diccionario genders, la cantidad de ejemplares
# macho, hembra, e indifinidos.
genders = {}
genders['f'] = 0
genders['m'] = 0
genders[None] = 0
for vs in graph.vs:
    genders[vs['sex']] += 1

# Imprimo en pantalla dichos valores
print u'Fracción de delfines machos:' + str(float(genders['m'])/number_of_vertices)
print u'Fracción de delfines hembras:' + str(float(genders['f'])/number_of_vertices)
print u'Fracción de delfines con género no especificado:' + str(float(genders[None])/number_of_vertices)


# Calculo la cantidad de links entre géneros que existen.
# No tomo en cuenta links que contengan un delfín con de género indefinido.
inter_gender_links = 0
for vs in graph.vs:
    neighbors = vs.neighbors()
    for neighbour in neighbors:
        if vs['sex'] != neighbour['sex'] and \
           vs['sex'] != None and neighbour['sex'] != None: 
            inter_gender_links += 1

# Real_inter_gender_links son efectivamente los links entre géneros de la red real
real_inter_gender_links = inter_gender_links / 2

print u'Enlaces entre géneros: ' + str(real_inter_gender_links)
print u'Fracción de enlaces entre géneros: ' + str(float(real_inter_gender_links)/number_of_links)


# Paso a sortear los géneros entre los vértices manteniendo
# la topología de la red inalterable. 
# De cada sorteo calculo el número de links entre especies
# de distinto género y devuelvo el histograma.

# Creo una lista con todas las etiquetas de género, respetando
# las cantidades de la red original.
list_of_genders = ['m'] * genders['m'] + ['f'] * genders['f'] + \
                  [None] * genders[None]

# Guardo en esta lista la cantidad de links entre géneros resultante 
# de cada realización al azar.
inter_gender_links_data = []

# Hago 10^6 realizaciones
nconf = 10**6
for conf in range(nconf):

    # Sorteo la lista de etiquetas de género y le asigno a cada 
    # delfín una nueva etiqueta. 
    i = 0
    random.shuffle(list_of_genders)
    for vs in graph.vs:
        vs['sex'] = list_of_genders[i]
        i += 1

    # Cuento los links entre géneros, luego del sorteo
    inter_gender_links = 0
    for vs in graph.vs:
        neighbors = vs.neighbors()
        for neighbour in neighbors:
            if vs['sex'] != neighbour['sex'] and \
              vs['sex'] != None and neighbour['sex'] != None: 
                inter_gender_links += 1

    aux = inter_gender_links / 2
    inter_gender_links_data.append(aux)

# Imprimo el valor medio y la desviación obtenida en el sorteo, de la 
# fracción de links entre géneros.
print u'Valor medio y desviación de la fracción de links entre géneros: '
print np.mean(inter_gender_links_data)/number_of_links,
print np.std(inter_gender_links_data)/number_of_links

# Genero el histograma de la distribución de links entre géneros.
# Incluyo el número de links entre géneros de la red real.
plt.hist(inter_gender_links_data, range = [40.5, 90.5], bins = 50, normed = True, label = u'Distribución nula')
plt.plot([real_inter_gender_links, real_inter_gender_links], [0.0, 0.05], '.-', markersize = 15, label = 'Red real')
plt.legend(loc = 2)
plt.xlabel(u'# de Links entre géneros')
plt.xlim([40, 90])
plt.grid('on')
plt.title(u'Número total de links = ' + str(number_of_links))
plt.savefig('Histograma.eps')
