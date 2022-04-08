from os import X_OK
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from vortex_generator_2 import Axis, SpatialGrid, FreqGrid, Phase, FourierField, AnaliticField

#setup parameters
m = 8E-4           #pixel size in sm
dataWidth = 1920   #Size of matrix
dataHeight = 1080 


f = 7.5 
l = 1.55E-4
r_l = 0.2

ri = 2E-1      #vortex radius
#wi = 10        #ring width
v_Ch = 2      #vortex charge
centerX = 0   #Vortex center
centerY = 0 

#precalculation
k = 2*pi/l                         #tot-Wave vector
v_Kr = k*ri/f                    #r-Wave vector
w = 1/r_l**2  #Vortex width


x_, y_ = Axis(dataWidth, dataHeight, m)
x2, y2, r = SpatialGrid(x_, y_, centerX, centerY, dataWidth, dataHeight, m)
xf, yf = FreqGrid(x_, y_, l, f)
phaseData = Phase(v_Kr, k, v_Ch, r, x2, y2)
field = FourierField(phaseData, w, r)
#Afield = AnaliticField(v_Ch, ri, wi, r, x2, y2)

fig, axes = plt.subplots(1, 2)
fig.set_figheight(5)
fig.set_figwidth(10)
axes[0].contourf(x2, y2, phaseData, 10, cmap='gray')
axes[0].grid()
axes[0].minorticks_on()
axes[0].grid(which='minor', color = 'white', linewidth = 0.08)

axes[1].contourf(xf, yf, field, 100, cmap='inferno')
axes[1].grid()
axes[1].minorticks_on()
axes[1].grid(which='minor', color = 'white', linewidth = 0.08)
#axes[2].contourf(x2, y2, Afield, 100, cmap='inferno')
#axes[2].grid()
#axes[2].minorticks_on()
#axes[2].grid(which='minor', color = 'white', linewidth = 0.08)

plt.show()