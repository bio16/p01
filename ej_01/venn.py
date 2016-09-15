#!/bin/env python3

import igraph 
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import seaborn as sns


files = ['yeast_AP-MS.txt','yeast_Y2H.txt','yeast_LIT.txt'] # nombres de los archivos
names = [ 'AP-MS','Y2H','LIT']                              # nombres 'bonitos' de los grafos
sets = []       #inicializo una lista de conjuntos
grafos = []     #inicilizo una lista de grafos
for file in files: 
    grafo = igraph.Graph.Read_Ncol(file) 
    gset = set(grafo.vs['name'])    # creamos un conjunto de las proteinas del grafo
    sets.append(gset)               # agregamos el conjunto a la lista de conjuntos
    grafo = grafo.as_undirected()  
    grafos.append(grafo)            # guardamos el grafo en la lista de grafos
                                    # (ya sabemos que no es dirigido)

# Analisis de covertura !
v = venn3(sets,names)   # funcion que crea un diagrama de venn con los conjuntos guardados anteriormente (y sus nombres)
v.get_patch_by_id('100').set_color(sns.xkcd_rgb['green'])       #\
v.get_patch_by_id('010').set_color(sns.xkcd_rgb['red'])         # => utilizamos los mismos colores que para los grafos
v.get_patch_by_id('001').set_color(sns.xkcd_rgb['purple'])      #/

filename = 'venn_'+'-'.join(names)      #\
plt.savefig(filename+'_covertura.pdf')  # => guardamos y mostramos el diagrama
plt.show()                              #/


# analisis de especificidad de los grafos !!
# sets[0] -> proteinas en AP-MS
# sets[1] -> proteinas en Y2H
# sets[2] -> proteinas en LIT
inter_all = sets[0] & sets[1] & sets[2]     # Calcula la interseccion de los 3 conjuntos de proiteinas
                                            # en python/conjuntos "&" es el operador de interseccion

# Esta seccion es analoga a la creacion de conjuntos anterior pero ahora para los links
# entre proteinas que esten en todos los grafos
link_sets = []
for grafo, name in zip(grafos,names):       
    subgrafo = grafo.subgraph(inter_all)    # crea el subgrafo a partir de la interseccion
    gset = set(subgrafo.get_edgelist())     # crea el conjunto de links del subgrafo
    link_sets.append(gset)                  # guardo el conjunto en link_sets
    subgrafo.save('subgrafo_'+name+'_all.gml')  # escribo un archivo con el subgrafo de la interseccion
                                                # quiza lo ploteo con plot.py

v = venn3(link_sets,names)  # crea el diagrama de venn
v.get_patch_by_id('100').set_color(sns.xkcd_rgb['green'])        #\                                                     
v.get_patch_by_id('010').set_color(sns.xkcd_rgb['red'])          # => utilizamos los mismos colores que para los grafos
v.get_patch_by_id('001').set_color(sns.xkcd_rgb['purple'])       #/
plt.savefig(filename+'_links.pdf')       # => guardamos y mostramos el diagrama
plt.show()                               #/


# guardo las intercciones entre 2 grafos por que quiza las ploteo !
inter_ap_ms_y2h = sets[0] & sets[1]     # interseccion AP-MS y Y2H
inter_ap_ms_lit = sets[0] & sets[2]     # interseccion AP-MS y LIT
inter_y2h_lit   = sets[1] & sets[2]     # interseccion Y2H y LIT
grafos[0].subgraph(inter_ap_ms_y2h).save('subgrafo_APMS_ap_ms_y2h.gml')
grafos[0].subgraph(inter_ap_ms_lit).save('subgrafo_APMS_ap_ms_lit.gml')
grafos[1].subgraph(inter_ap_ms_y2h).save('subgrafo_Y2H_ap_ms_y2h.gml')
grafos[1].subgraph(inter_y2h_lit).save('subgrafo_Y2H_y2h_lit.gml')
grafos[2].subgraph(inter_ap_ms_lit).save('subgrafo_LIT_ap_ms_lit.gml')
grafos[2].subgraph(inter_y2h_lit).save('subgrafo_LIT_y2h_lit.gml')
