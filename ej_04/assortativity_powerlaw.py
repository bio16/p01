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
argparser.add_argument('--loglog','-l',action='store_true',
        help='loglog scale for the plot')

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

###############################################################################
# Creacion del grafo a partir del archivo de entrada
###############################################################################
import numpy as np

grafo_adjlist = grafo.get_adjlist()
grafo_degree  = grafo.degree()

#creamos un diccionario que contenga todos los nodos que son vecinos de un nodo
#de grado 'degree'
neighborhood = {}
for node,degree in enumerate(grafo_degree):
    for neighbor in grafo_adjlist[node]:
        # aniade el grado de los vecinos de los nodos de grado 'degree'
        try:
            if neighbor not in neighborhood[degree]:
                neighborhood[degree].append(neighbor)
        # crea nueva lista si la lista para ese grado no existe
        except:
            neighborhood[degree] = [neighbor]


#creamos un vector (k, <k_neighborhood>)
grafo_nbh_degree = []   # neighborhood mean degree (knn)
for degree,nodes in neighborhood.items():
    aux = []
    for node in nodes:
        aux.append(grafo_degree[node])
    grafo_nbh_degree.append([degree,np.mean(aux)])


# Reodenamos los datos para facilitar manejo
grafo_nbh_degree = np.array(grafo_nbh_degree).T
grafo_nbh_degree = np.sort(grafo_nbh_degree,axis=1)

###############################################################################
#  Sobrecarga del la clase power law model de lmfit
#  para fiteo de knn(k)
###############################################################################
import lmfit as lmf

class PowerLawModel(lmf.models.PowerLawModel):
    """
    Sobrecarga de la clase PowerLawModel de lmfits
    """
    def function(self,data,params):
        prefix = self.prefix
        
        amplitude = params[prefix+'amplitude'].value
        exponent  = params[prefix+'exponent'].value
        return amplitude*np.power(data,exponent)
        
power_model = PowerLawModel(prefix='power_')
##########
# Fiteo
###########
params = power_model.guess(grafo_nbh_degree[1,:],x=grafo_nbh_degree[0,:])
result = power_model.fit(grafo_nbh_degree[1,:],params,x=grafo_nbh_degree[0,:])
print(result.fit_report())

###############################################################################
# Ploteo
###############################################################################
import matplotlib.pyplot as plt

fig,subplot = plt.subplots(ncols=1,nrows=1)

min_degree = np.min(grafo_nbh_degree[0,:])
max_degree = np.max(grafo_nbh_degree[0,:])

fit_x = np.linspace(min_degree,max_degree,100)
fit_y = result.model.function(fit_x,result.params)

subplot.plot(fit_x,fit_y,label='power law fit')
subplot.plot(grafo_nbh_degree[0,:],grafo_nbh_degree[1,:],'.', label='data')
subplot.set_xlabel('degree (k)')
subplot.set_ylabel('mean neighborhood degree (<k_nn>)')

if args.loglog:
    subplot.set_yscale('log')
    subplot.set_xscale('log')
    filename += '_loglog'

subplot.legend(loc='best')

plt.savefig('schemes/'+filename+'.pdf')
plt.show()
