import astropy.units as u
import pyoptica as po
import numpy as np
import matplotlib.pyplot as plt
from test import BesselMask


ch = 10
a = 10000/u.m
w = 1 *u.mm
wavelength = 1550 * u.nm

pixel_scale = 8 * u.um
npix = 1080

f = 0.15 * u.m
radius = 1 * u.mm
lens = po.ThinLens(radius, f)
mask = BesselMask(a, ch, w)
fs = po.FreeSpace(f, 'ASPW')

wf = po.Wavefront(wavelength, pixel_scale, npix)
wf = wf*mask*fs*lens*fs
plt.imshow(wf.intensity)
plt.colorbar()
plt.show()