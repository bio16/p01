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
grafo = nx.Graph(igrafo.get_edgelist())

# matriz de probabilidad de interaccion entre nodos de grado k_i y k_j
mixing = np.rot90(nx.degree_mixing_matrix(grafo,normalized=True))
for i in range(mixing.shape[0]):
    for j in range(mixing.shape[1]):
        if mixing[i,j] == 0:
            mixing[i,j] = -3e-3


k_nn = nx.average_neighbor_degree(grafo)
degrees = list(k_nn.keys())
###############################################################################
# Ploteo
###############################################################################
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use(['seaborn-talk','seaborn-whitegrid'])

fig,subplot = plt.subplots(ncols=1,nrows=1)

cmap = sns.cubehelix_palette(8, start=0.5, rot=-.75,light=0.9,as_cmap=True)
plt.imshow(mixing, interpolation='none', cmap=cmap
        ,extent=(0.5,np.shape(mixing)[0]+0.5,0.5,np.shape(mixing)[1]+0.5)
            )
plt.colorbar()

subplot.grid(b=False)
subplot.set_xlabel('$k_i$')
subplot.set_ylabel('$k_j$')



plt.savefig('schemes/mixing_'+filename+'.pdf')
plt.show()
