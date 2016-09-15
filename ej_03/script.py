#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
"""
ejerc 03, prt 1
"""
import igraph
from pylab import figure, hist, show, close
import numpy as np
from numpy import log10
"""
+++++++++++++  PARTE A ++++++++++++++
"""

ir = igraph.Graph.Read_GML('../data/as-22july06.gml')

lk = log10(ir.degree())
hc, hx_ = np.histogram(lk, bins=20)
hc_orig = np.copy(hc)
hx = 0.5*(hx_[:-1] + hx_[1:])
N  = hc.sum()
#hc /= 1.*N*(hx[1]-hx[0])
A  = 1.*(hc*(hx_[1:] - hx_[:-1])).sum() # area of the un-normalized distribution
hc = np.float32(hc) # para normalizar con punto flotante
hc /= A # ahora 'hc' es una distribucion de probabilidad (with area=1.0)

m, b = np.polyfit(hx, log10(hc), deg=1)

fig = figure(1, figsize=(6,4))
ax  = fig.add_subplot(111)

label = 'N:%d' % N
ax.plot(pow(10.,hx), hc, '-o', label=label)
# fit curve
ax.plot(pow(10.,hx), pow(10.,m*hx+b), 'r--', lw=3, alpha=0.6, label='spectral index: %2.2f'%m)

ax.set_xlabel('k')
ax.set_ylabel('$P_K$')
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True)
ax.legend(loc='best')

fig.savefig('./Pk.png', dpi=150, bbox_inches='tight')
close(fig)



"""
+++++++++++++  PARTE B ++++++++++++++
"""
#--- ahora intentamos con igraph, para q nos estime 
#    el "kmin" (no es lo mismo q el `xmin` del igraph)
ih  = 1./hc_orig # if Pk~k^{-alpha} --> Pk^{-1}~k^alpha

# the xmin value of igraph refers to the left border if
# `Pk` is ascending, so I give it the inverse as argument.
# As python-igraph is a wrapper around C code, see:
# http://igraph.org/c/doc/igraph-Nongraph.html
res = igraph.power_law_fit(ih)
print(res.summary()) 
cc = ih>=res.xmin # True for the correct fit, according to igraph

fig = figure(1, figsize=(6,4))
ax  = fig.add_subplot(111)

label = 'N:%d' % N
# ploteo todos los valores de Pk
ax.plot(pow(10.,hx), hc, '-o', c='None',label='all Pk values')
# ploteo solo los valores q escogio igraph
ax.plot(pow(10.,hx)[cc], hc[cc], '-o', label='used for fit')
#--- fit curve with igraph
ax.plot(pow(10.,hx), pow(10.,-res.alpha*hx+b+.3), 'r--', lw=3, alpha=0.6, label='igraph fit: %2.2f'%-res.alpha)
ax.legend(loc='best')
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True)
fig.savefig('./igraph_version.png',dpi=150,bbox_inches='tight')
close(fig)

#EOF
