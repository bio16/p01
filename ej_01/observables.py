#!/bin/env python3
import numpy as np
import argparse as arg
import igraph 


#se crean argumentos amigables para usar el script con diferentes archivos
argparser = arg.ArgumentParser(description='')
argparser.add_argument('file',help='graph file')
args = argparser.parse_args()


grafo = igraph.Graph.Read_Ncol(args.file) # se lee el archivo dado y se crea un grafo

#se imprime nombre del archivo para no olvidarse
print('Nombre del archivo:', args.file)
print()

#Analisis si la matriz es dirigida o no
#calculo matriz de adyacencia
adj = np.array(grafo.get_adjacency().data)
adj = adj - np.diag(np.diag(adj))   # extraemos diagonal 

sim_adj = adj + adj.T   # proyectamos la matriz adj en su version simetrica

dirigida = True                         # Parto del supuesto que ES dirigida
if np.all(sim_adj.flat < 2):            # pero si la proyeccion simetrica de adj
    dirigida = False                    # tiene todos sus elementos < 2, es MUY probable 
    grafo = grafo.as_undirected()       # que sea NO-DIRIGIDA
print('es dirigido?:',dirigida)

# Calculo e impresion de observables
print('numero de nodos :',grafo.vcount())
print('numero de links :',grafo.ecount())
print('k-out medio :',np.sum(grafo.outdegree())/grafo.vcount())
print('k-in medio: ',np.sum(grafo.indegree())/grafo.vcount())
print('grado maximo [in/out]:',np.max(grafo.indegree()),np.max(grafo.outdegree()))
print('grado minimo [in/out]:',np.min(grafo.indegree()),np.min(grafo.outdegree()))
print('densidad :',grafo.density(loops=True))
print('coeficiente de clustering (local/media):',grafo.transitivity_avglocal_undirected())
print('coeficiente de clustering (global/triangulo):',grafo.transitivity_undirected())
print('diametro:',grafo.diameter())
print()

