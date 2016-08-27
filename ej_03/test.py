#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import igraph
from pylab import figure, hist, show, close
import numpy as np
from numpy import log10

ir = igraph.Graph.Read_GML('../data/as-22july06.gml')
#igraph.plot(ir, target='test.png')

lk = log10(ir.degree())
hc, hx_ = np.histogram(lk, bins=20)
hx = 0.5*(hx_[:-1] + hx_[1:])

m, b = np.polyfit(hx, log10(hc), deg=1)

fig = figure(1, figsize=(6,4))
ax  = fig.add_subplot(111)

label = 'N:%d' % hc.sum()
ax.plot(pow(10.,hx), hc, '-o', label=label)
# fit curve
ax.plot(pow(10.,hx), pow(10.,m*hx+b), 'r--', lw=3, alpha=0.6, label='spectral index: %2.2f'%m)

ax.set_xlabel('k')
ax.set_ylabel('$P_K$')
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True)
ax.legend(loc='best')

fig.savefig('Pk.png', dpi=150, bbox_inches='tight')
close(fig)

#print('grado medio:',np.mean(g.degree()))
#print('grado maximo:',np.max(g.degree()))
#print('diametro:',g.diameter())
#print('average path length:',g.average_path_length())
#print('shortest path:',np.min(g.shortest_paths()))
#EOF
