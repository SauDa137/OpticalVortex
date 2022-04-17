from re import A
import astropy.units as u
import numpy as np
from numpy import pi
from pyoptica import BaseOpticalElement
from VortexFunctions import CreatSpatialAxis, CreateSpatialGrid


class BesselMask(BaseOpticalElement):
    @u.quantity_input(a=1/u.m, w=u.m)
    def __init__(self, a, b, w):
        self.a = a
        self.b = b/u.rad
        self.w = w

    def amplitude_transmittance(self, wavefront):
        x, y = wavefront.x, wavefront.y
        xy_squared = x ** 2 + y ** 2
        t1 = np.exp(-xy_squared/self.w**2)
        intense = np.where(
            True, t1, 1
        )
        return intense

    def phase_transmittance(self, wavefront):
        x, y = wavefront.x, wavefront.y
        xy_squared = x ** 2 + y ** 2
        theta = np.arctan2(y, x)
        t1 = np.exp(- 1j * (self.a*np.sqrt(xy_squared) + self.b*theta))
        phi = np.where(
            True, t1, 1
        )
        return phi
