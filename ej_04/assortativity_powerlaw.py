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

###############################################################################
# Creacion del grafo a partir del archivo de entrada
###############################################################################
import igraph 
import networkx as nx
import numpy as np

igrafo = igraph.read(args.file,format=args.format)
igrafo = igrafo.as_undirected()

grafo = nx.Graph(igrafo.get_edgelist())


#calcula el valor de asortatividad neutro
#   k_nn(k) = <k^2>/<k>
degrees = np.array(igrafo.degree()) # momento 1 de k
ddegrees = np.power(degrees,2)      # momento 2 de k

k_neutro = np.mean(ddegrees)/np.mean(degrees)

# calculo los k_nn(k) y los ordeno por valor de grado k
knn = nx.average_degree_connectivity(grafo)
knn = np.array([(k,v) for k,v in knn.items()])

###############################################################################
#  Sobrecarga del la clase power law model de lmfit
#  para fiteo de knn(k)
###############################################################################
import lmfit as lmf

#se define funcion para plotear
        
def power(x,a,m):
    """
    power(x) = a*x^m

    x: datos
    a: amplitud
    m: exponente
    """
    return a*np.power(x,m)


lin_model = lmf.models.LinearModel()

##########
# Fiteo
###########
#fiteo linear del log de los datos
lparams = lin_model.guess(np.log(knn[:,1]),x=np.log(knn[:,0]))
lresult = lin_model.fit(np.log(knn[:,1]),lparams,x=np.log(knn[:,0]))
print(lresult.fit_report())


###############################################################################
# Ploteo
###############################################################################
import matplotlib.pyplot as plt
import seaborn as sns
fig,subplot = plt.subplots(ncols=1,nrows=1)
plt.style.use(['seaborn-talk','seaborn-whitegrid'])

#si se setea loglog se setean ejes
filename = '-'.join(args.file.split('/')[-1].split('.'))
if args.loglog:
    subplot.set_yscale('log')
    subplot.set_xscale('log')
    filename += '_loglog'

#ploteamos los datos
subplot.plot(knn[:,0],knn[:,1],'.',label='datos')

#ploteo k_nn neutro
x = subplot.get_xlim()   # para dibujar una linea de extremo a extremo
y = [k_neutro, k_neutro] # horizontal
subplot.plot(x,y,'k--',label='Prediccion random')


#ploteo del modelo linear
x = np.linspace(x[0],x[1], 1000)  # utilizo los valores ya calculados en el grafico anterior
lin_y = power(x, np.exp(lresult.params['intercept'].value), lresult.params['slope'])
subplot.plot(x,lin_y, label='fit')



#propiedades del grafico
subplot.set_xlabel('degree ($k$)')
subplot.set_ylabel('mean neighborhood degree ($k_{nn}(k)$)')
subplot.legend(loc='best')

plt.savefig('schemes/assort_'+filename+'.pdf')
plt.show()
