#!/bin/env python3

###############################################################################
# Parseado de argumentos del script
###############################################################################
import argparse as arg
import sys
AcceptedFormats = [None,'gml','ncol','lgl','graphdb','graphml','graphmlz',
        'net','pajek','dimacs','edge','edgelist','edges','adjacency','pickle',
        'picklez']
argparser = arg.ArgumentParser(description='',prog=sys.argv[0])
argparser.add_argument('file',help='graph file')
argparser.add_argument('--format','-f', default=None,
        help='force format of the file (default:autodetect)',
        choices=AcceptedFormats)
argparser.add_argument('--loglog','-l',action='store_true',
        help='loglog scale for the plot')

args = argparser.parse_args()
if args.format not in AcceptedFormats:
    print('Formato %s no aceptado'%args.format)
    sys.exit(1)

filename = '-'.join(args.file.split('/')[-1].split('.'))
###############################################################################
# Creacion del grafo a partir del archivo de entrada
###############################################################################
import igraph 
import networkx as nx
import numpy as np

igrafo = igraph.read(args.file,format=args.format)
grafo = nx.DiGraph(igrafo.get_edgelist())

# matriz de probabilidad de interaccion entre nodos de grado k_i y k_j
mixing = np.rot90(nx.degree_mixing_matrix(grafo,normalized=True))

k_nn = nx.average_neighbor_degree(grafo)
degrees = list(k_nn.keys())
print(mixing.shape)
print(nx.degree_mixing_dict(grafo,normalized=True))
###############################################################################
# Ploteo
###############################################################################
import matplotlib.pyplot as plt
import seaborn as sns
fig,subplot = plt.subplots(ncols=1,nrows=1)

plt.imshow(mixing, interpolation='none', cmap=sns.cubehelix_palette(8, start=.5, rot=-.75,as_cmap=True)
            ,extent=(0.5,np.shape(mixing)[0]+0.5,0.5,np.shape(mixing)[1]+0.5)
            )
plt.colorbar()


subplot.set_xlabel('$k_i$')
subplot.set_ylabel('$k_j$')



plt.savefig('schemes/mixing_'+filename+'.pdf')
plt.show()
