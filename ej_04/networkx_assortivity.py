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
import pandas as pd

igrafo = igraph.read(args.file,format=args.format)
grafo = nx.DiGraph(igrafo.get_edgelist())

knn = nx.k_nearest_neighbors(grafo)

knn = np.sort(np.array([(k,v) for k,v in knn.items()]),axis=0)

###############################################################################
#  Sobrecarga del la clase power law model de lmfit
#  para fiteo de knn(k)
###############################################################################
import lmfit as lmf

#se definen funciones para plotear
def lin(x,n,m):
    """
    lin(x) = n*x + m

    x: datos
    n: pendiente
    m: interseccion con el eje
    """
    return n*x+m
        
def power(x,a,m):
    """
    power(x) = a*x^m

    x: datos
    a: amplitud
    m: exponente
    """
    return a*np.power(x,m)


lin_model = lmf.models.LinearModel()
power_model = lmf.models.PowerLawModel()
##########
# Fiteo
###########
#fiteo linear del log de los datos
lparams = lin_model.guess(np.log(knn[:,1]),x=np.log(knn[:,0]))
lresult = lin_model.fit(np.log(knn[:,1]),lparams,x=np.log(knn[:,0]))
print(lresult.fit_report())

#power law model
pparams = power_model.guess(knn[:,1],x=knn[:,0])
presult = power_model.fit(knn[:,1],pparams,x=knn[:,0])
print(presult.fit_report())

###############################################################################
# Ploteo
###############################################################################
import matplotlib.pyplot as plt
import seaborn as sns
fig,subplot = plt.subplots(ncols=1,nrows=1)

subplot.plot(knn[:,0],knn[:,1],'.',label='datos')

#ploteo de la power law fit
x = np.linspace(np.min(knn[:,0]),np.max(knn[:,0]), 1000)
power_y = power(x, presult.params['amplitude'], presult.params['exponent'])
subplot.plot(x,power_y, label='power_log_fit')

#ploteo del modelo linear
x = np.linspace(np.min(knn[:,0]),np.max(knn[:,0]), 1000)
lin_y = power(x, np.exp(lresult.params['intercept'].value), lresult.params['slope'])
subplot.plot(x,lin_y, label='linear_fit')

subplot.set_xlabel('degree ($k$)')
subplot.set_ylabel('mean neighborhood degree ($<k_nn>$)')

if args.loglog:
    subplot.set_yscale('log')
    subplot.set_xscale('log')
    filename += '_loglog'


subplot.legend(loc='best')

plt.savefig('schemes/assort_'+filename+'.pdf')
plt.show()
