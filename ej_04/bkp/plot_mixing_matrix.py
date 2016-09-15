#!/bin/env/python3

from graph_tool.all import * 
import matplotlib.pyplot as plt
import seaborn as sns
import argparse as arg
import numpy as np

# seccion de argumentos del programa
AcceptedFormats = [ 'auto','gml','gt','graphml','xml','dot','csv' ]     # formatos soportados
vcolors = list(sns.xkcd_rgb.keys()) # nombres de colores (http://xkcd.com/color/rgb/)

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file',help='graph file')
argparser.add_argument('--format','-f', default='auto',
        help='force format of the file (default:autodetect)',choices=AcceptedFormats)
argparser.add_argument('--is_directed','-d',action='store_true',help='directed graph')

args = argparser.parse_args()

#importa el grafo
if args.format == 'csv':   # si el formato es una lista de links hay que tratarlo distinto (csv)
    graph = load_graph_from_csv(args.file,string_vals=True,directed=args.is_directed,
                csv_options={"delimiter": "\t", "quotechar": "#"})
else:  # si no es csv, que lo lea tranqui..
    graph = load_graph(args.file,fmt=args.format)

#chequea que todo sea como "debe ser"
print('chequeando...',args.file)
print('vertices',len(list(graph.vertices()))) #numero de vertices
print('edges',len(list(graph.edges())))       #numero de links

hist = combined_corr_hist(graph, "total", "total")

# seteo de algunas argumentos de la creacion del grafo
filename = '-'.join(args.file.split('/')[-1].split('.'))    #extraccion de simbolos raros en el nombre del archivo


plt.style.use(['seaborn-talk','seaborn-whitegrid'])
fig,subplot = plt.subplots(ncols=1,nrows=1)

cmap = sns.cubehelix_palette(8, start=0.5, rot=-.75,light=0.9,as_cmap=True)
plt.imshow(hist[0].T, interpolation='nearest', cmap=cmap
        #,extent=(0.5,np.shape(mixing)[0]+0.5,0.5,np.shape(mixing)[1]+0.5)
            )
plt.colorbar()

subplot.grid(b=False)
subplot.set_xlabel('$k_i$')
subplot.set_ylabel('$k_j$')



plt.savefig('schemes/mixing_'+filename+'.pdf')
plt.show()
