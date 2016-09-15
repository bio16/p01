import numpy as np
import argparse as arg
import igraph 
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

argparser = arg.ArgumentParser(description='')
argparser.add_argument('files',help='graph file',nargs='+')
argparser.add_argument('--names','-n',help='graph names',nargs='+')

args = argparser.parse_args()

sets = []
names = []
grafos = []
for file in args.files:
    grafo = igraph.Graph.Read_Ncol(file)
    gset = set(grafo.vs['name'])
    sets.append(gset)
    names.append(file)
    grafo = grafo.as_undirected()
    grafos.append(grafo)


venn3(sets,names)
filename = 'venn_'+'-'.join(names)
plt.savefig(filename+'.pdf')
plt.show()

