#!/bin/env python3

###############################################################################
# Parseado de argumentos del script
###############################################################################
import argparse as arg
import sys
argparser = arg.ArgumentParser(description='',prog=sys.argv[0])
argparser.add_argument('file',help='graph file')
argparser.add_argument('--format','-f', default=None,
        help='force format of the file (default:autodetect)')

args = argparser.parse_args()
AcceptedFormats = [None,'gml','ncol','lgl','graphdb','graphml','graphmlz',
        'net','pajek','dimacs','edge','edgelist','edges','adjacency','pickle',
        'picklez']
if args.format not in AcceptedFormats:
    print('Formato %s no aceptado'%args.format)
    sys.exit(1)

filename = args.file.split('/')[-1]
###############################################################################
# Creacion del grafo a partir del archivo de entrada
###############################################################################
import igraph 

grafo = igraph.read(args.file,format=args.format)
grafo = grafo.as_undirected()
###############################################################################
# Creacion del grafo a partir del archivo de entrada
###############################################################################
import numpy as np

# listas ordenadas por nodo de vecinos (adjlist) y grados (degree)
grafo_adjlist = grafo.get_adjlist() 
grafo_degree  = grafo.degree()

# calculo del coeficiente de asortividad de newman 
#
#       s1*se - s2*s2
#   r = -------------
#       s2*s3 - s2*s2
#
s1 = np.sum(grafo_degree)
s2 = np.sum(np.power(grafo_degree,2))
s3 = np.sum(np.power(grafo_degree,3))

s22 = s2*s2

se = 0
for node,neighbors in enumerate(grafo_adjlist):
    neighbors_degree = []
    for n in neighbors:
        neighbors_degree.append(grafo_degree[n])
    se += grafo_degree[node] * np.sum(neighbors_degree)

#calculamos la asortatividad por 2 metodos... para asegurarse !
assortativity = (s1*se - s22)/(s1*s3 - s22)
igraph_assortativity = grafo.assortativity_degree()

print('Newman assortativity:',assortativity)
print('igraph Newman assortativity:',igraph_assortativity)

