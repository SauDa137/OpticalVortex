from os import X_OK
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

def CreatSpatialAxis(dataWidth, dataHeight, PixelSize):
    x_axis = np.linspace(0,dataWidth*PixelSize,dataWidth)
    y_axis = np.linspace(0,dataHeight*PixelSize,dataHeight)
    return x_axis, y_axis

def CreateSpatialGrid(x_axis, y_axis, centerX, centerY, dataWidth, dataHeight, PixelSize):
    #create spatial grid
    x_grid, y_grid = np.meshgrid(x_axis, y_axis)
    #centered grid
    x_grid_centered = x_grid - dataWidth*PixelSize/2+centerX
    y_grid_centered = y_grid - dataHeight*PixelSize/2+centerY
    r = np.sqrt(x_grid_centered**2+y_grid_centered**2)
    return x_grid_centered, y_grid_centered, r

def CreateFrequencyGrid(x_axis, y_axis, waveLengthScaled, lenseFocalDistanceScaled):
    #create frequency grid
    kx = np.fft.fftfreq(len(x_axis), np.diff(x_axis)[0]) 
    ky = np.fft.fftfreq(len(y_axis), np.diff(y_axis)[0])
    kx_grid, ky_grid = np.meshgrid(kx,ky)
    return np.fft.fftshift(kx_grid)*waveLengthScaled*lenseFocalDistanceScaled, np.fft.fftshift(ky_grid)*waveLengthScaled*lenseFocalDistanceScaled

def BesselVortexMask(vortexWaveVectorRadial, vortexWaveVector, vortexCharge, r, x_grid_centered, y_grid_centered):
    #phase mask
    return  vortexWaveVector*np.arcsin(vortexWaveVectorRadial/vortexWaveVector)*r + vortexCharge*np.arctan2(y_grid_centered,x_grid_centered)

def Mask2FieldFourier(phaseData, w, r):
    #field from mask
    Edata = np.exp(-w*r**2)*np.cos(phaseData)
    ft_Edata = np.fft.fft2(Edata)
    return abs(np.fft.fftshift(ft_Edata)+100*np.exp(-r**2/4E-4))**2

def Mask2FielAnalitic(vortexCharge, vortexRadius, vortexWidth, r, x_grid_centered, y_grid_centered):
    #field from formula
    return abs( np.cos(vortexCharge*np.arctan2(y_grid_centered,x_grid_centered)+ pi/2*(vortexCharge-1))*np.exp(-(r - vortexRadius)**2/vortexWidth**2) )**2

