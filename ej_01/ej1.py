import numpy as np
import matplotlib.pyplot as plt
import igraph 



ap_ms = igraph.Graph.Read_Ncol('yeast_AP-MS.txt')
lit = igraph.Graph.Read_Ncol('yeast_LIT.txt')
y2h = igraph.Graph.Read_Ncol('yeast_Y2H.txt')

#igraph.plot(ap_ms)
#igraph.plot(lit)
#igraph.plot(y2h)


print('numero de nodos ap-ms:',ap_ms.vcount())
print('numero de nodos y2h:  ',y2h.vcount())
print('numero de nodos lit:  ',lit.vcount())

print()

print('numero de links ap-ms:',ap_ms.ecount())
print('numero de links lit:  ',lit.ecount())
print('numero de links y2h:  ',y2h.ecount())

print()

print('numero de k-out ap-ms:',np.sum(ap_ms.outdegree())/ap_ms.vcount())
print('numero de k-in ap-ms: ',np.sum(ap_ms.indegree())/ap_ms.vcount())
print('numero de k-out ap-ms:',np.sum(lit.outdegree())/lit.vcount())
print('numero de k-in ap-ms: ',np.sum(lit.indegree())/lit.vcount())
print('numero de k-out ap-ms:',np.sum(y2h.outdegree())/y2h.vcount())
print('numero de k-in ap-ms: ',np.sum(y2h.indegree())/y2h.vcount())


#u = open(1, 'w', encoding='utf-8', closefd=False)
#
#data = pd.read_csv("lista_curso.csv",encoding='utf-8')
#data = data.replace(np.nan,0)
#
#names_data = data.drop(data.columns[range(14)] ,axis=1)
#
#print(names_data.columns,file=u)
#print(names_data,file=u)
#
#node_names = data['Nombre'].values
#print(node_names,file=u)
#
#
#values = names_data.values
#g = igraph.Graph.Adjacency(values.tolist())
#
#g.es['weight'] = values[values.nonzero()]
#g.vs['labels'] = node_names
#g.vs['carrera'] = data['Carrera de grado']
#
##hist(g.degree(),bins=25)
##show()
#
#print(g.degree(),file=u)
##igraph.plot(g, vertex_label=g.vs['carrera'])
#
#
#print('grado medio:',np.mean(g.degree()))
#print('grado maximo:',np.max(g.degree()))
#print('diametro:',g.diameter())
#print('average path length:',g.average_path_length())
#print('shortest path:',np.min(g.shortest_paths()))
#
