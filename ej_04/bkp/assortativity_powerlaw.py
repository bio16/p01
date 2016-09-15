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
import numpy as np

grafo = igraph.read(args.file,format=args.format)
grafo = grafo.as_undirected()
#calcula el valor de asortatividad neutro
#   k_nn(k) = <k^2>/<k>
degrees = np.array(grafo.degree()) # momento 1 de k
ddegrees = np.power(degrees,2)      # momento 2 de k

k_neutro = np.mean(ddegrees)/np.mean(degrees)

###############################################################################
# Creacion del grafo a partir del archivo de entrada
###############################################################################

grafo_adjlist = grafo.get_adjlist()
grafo_degree  = grafo.degree()
#Extraer la matriz de adyacencia es muy pesado, mejor tomar lista de vecinos y 
#promediar sobre ellos


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
#grafo_nbh_degree = np.sort(grafo_nbh_degree,axis=1)



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
lparams = lin_model.guess(np.log(grafo_nbh_degree[1,:]),x=np.log(grafo_nbh_degree[0,:]))
lresult = lin_model.fit(np.log(grafo_nbh_degree[1,:]),lparams,x=np.log(grafo_nbh_degree[0,:]))
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
subplot.plot(grafo_nbh_degree[0,:],grafo_nbh_degree[1,:],'.', label='data')

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

