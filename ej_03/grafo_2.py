import numpy as np
import matplotlib.pyplot as plt
from pylab import hist,show
import igraph 
import pandas as pd

u = open(1, 'w', encoding='utf-8', closefd=False)

data = pd.read_csv("lista_curso.csv",encoding='utf-8')
data = data.replace(np.nan,0)

names_data = data.drop(data.columns[range(14)] ,axis=1)

print(names_data.columns,file=u)
#print(names_data,file=u)

node_names = data['Nombre'].values
#print(node_names,file=u)


values = names_data.values
g = igraph.Graph.Adjacency(values.tolist())

g.es['weight'] = values[values.nonzero()]
g.vs['labels'] = node_names
g.vs['carrera'] = data['Carrera de grado']

#hist(g.degree(),bins=25)
#show()

print(g.degree(),file=u)
#igraph.plot(g, target='./test.png', vertex_label=g.vs['carrera'])


print('grado medio:',np.mean(g.degree()))
print('grado maximo:',np.max(g.degree()))
print('diametro:',g.diameter())
print('average path length:',g.average_path_length())
print('shortest path:',np.min(g.shortest_paths()))

