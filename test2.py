import astropy.units as u
import pyoptica as po
import numpy as np
import matplotlib.pyplot as plt
from test import BesselMask, GaussMask, Mirror
from numpy import pi

beamWidth = 2 *u.mm
beamWavelength = 1550 * u.nm

lensFocus = 7.5 * u.cm
lensRadius = 15 * u.mm

pixel_scale = 8 * u.um
npix = 1080
R=0.1

vortexRadius  = 2 *u.mm 
vortexCharge = 0
mask2lensD = lensFocus
lens2camD = 2*lensFocus 
vortexWaveVector = 2*pi/beamWavelength
vortexWaveVectorRadial = vortexRadius*vortexWaveVector/lensFocus 
BesselPeriod = vortexWaveVector*np.arcsin(vortexWaveVectorRadial/vortexWaveVector)/u.rad

lens = po.ThinLens(lensRadius, lensFocus)
gaussMask = GaussMask(beamWidth)
besselMask = BesselMask(BesselPeriod, vortexCharge)
mirror = Mirror(0.1)

fs1 = po.FreeSpace(mask2lensD, 'ASPW')
fs2 = po.FreeSpace(lens2camD, 'ASPW')

waveFront = po.Wavefront(beamWavelength, pixel_scale, npix)

waveFront_signal = waveFront*gaussMask*besselMask*fs1*lens*fs2*lens*fs1
waveFront_noise = waveFront*gaussMask*mirror*fs1*lens*fs2*lens*fs1
_ = waveFront_noise.plot(intensity='default', phase='default')
_ = waveFront_signal.plot(intensity='default', phase='default')
plt.show()