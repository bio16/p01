import numpy as np
import matplotlib.pyplot as plt
import argparse as arg
import igraph 
import networkx as nx

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file',help='graph file')
argparser.add_argument('--plot','-p',help='plot graph',action='store_true')

args = argparser.parse_args()
filename = args.file.split('/')[-1]

grafo = igraph.Graph.Read_Ncol(args.file)

# Imprime en pantalla los observables del grafo
print('Nombre del archivo:', args.file)
print()
print('es dirigido?:',grafo.is_directed())
print('es simple?:',grafo.is_simple())
print('numero de nodos :',grafo.vcount())
print('numero de links :',grafo.ecount())
print('numero de k-out :',np.sum(grafo.outdegree())/grafo.vcount())
print('numero de k-in : ',np.sum(grafo.indegree())/grafo.vcount())
print('grado maximo [in/out]:',np.max(grafo.indegree()),np.max(grafo.outdegree()))
print('grado minimo [in/out]:',np.min(grafo.indegree()),np.min(grafo.outdegree()))
print('densidad :',grafo.density(loops=True))
print('coeficiente de clustering (local/media):',grafo.transitivity_avglocal_undirected())
print('coeficiente de clustering (global/triangulo):',grafo.transitivity_undirected())
print('diametro:',grafo.diameter())
print()

if args.plot:
#grafica el grafo con networkx (maneja mas amablemente las figuras)
    grafo_nx = nx.DiGraph(grafo.get_edgelist())
    nx.draw(grafo_nx,node_size=50, width=0.3, alpha=0.9)

    plt.savefig('./schemes/'+filename+'.pdf')
