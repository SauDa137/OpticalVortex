from re import A
import astropy.units as u
import numpy as np
from numpy import pi
from pyoptica import BaseOpticalElement
from VortexFunctions import CreatSpatialAxis, CreateSpatialGrid


class GaussMask(BaseOpticalElement):
    @u.quantity_input(a=1/u.m, w=u.m)
    def __init__(self, w):
        self.w = w

    def amplitude_transmittance(self, wavefront):
        x, y = wavefront.x, wavefront.y
        xy_squared = x ** 2 + y ** 2
        t1 = np.exp(-xy_squared/self.w**2)
        intense = np.where(
            np.sqrt(xy_squared)<=wavefront.npix*wavefront.pixel_scale, t1, 1
        )
        return intense

    def phase_transmittance(self, wavefront):
        return np.exp(1.j * np.zeros_like(wavefront.phase))


class BesselMask(BaseOpticalElement):
    @u.quantity_input(a=1/u.m, w=u.m)
    def __init__(self, a, b):
        self.a = a
        self.b = b/u.rad

    def amplitude_transmittance(self, wavefront):
        return np.ones_like(wavefront.amplitude)

    def phase_transmittance(self, wavefront):
        x, y = wavefront.x, wavefront.y
        xy_squared = x ** 2 + y ** 2
        theta = np.arctan2(y, x)
        t2 = np.exp(- 1.j * (self.a*np.sqrt(xy_squared) + self.b*theta))
        phi = np.where(
            np.sqrt(xy_squared)<=wavefront.npix*wavefront.pixel_scale, t2, 1
        )
        return phi

class PhaseRotation(BaseOpticalElement):
    def __init__(self, phi):
        self.phi = phi

    def amplitude_transmittance(self, wavefront):
        return np.ones_like(wavefront.amplitude)

    def phase_transmittance(self, wavefront):
        t3 = np.exp(1.j*self.phi)
        phase = np.where(
            True, t3, 1
        )
        return phase

class Mirror(BaseOpticalElement):
    def __init__(self, R):
        self.R = R

    def amplitude_transmittance(self, wavefront):
        return self.R*np.ones_like(wavefront.amplitude)

    def phase_transmittance(self, wavefront):
        t3 = np.exp(1.j*pi)
        phase = np.where(
            True, t3, 1
        )
        return phase
