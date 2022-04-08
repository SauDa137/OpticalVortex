from os import X_OK
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt


def PhaseMatrix(dataWidth, dataHeight, centerX, centerY):
    X = np.arange(-dataWidth/2, dataWidth/2)
    Y = np.arange(-dataHeight/2, dataHeight/2)
    x, y = np.meshgrid(X, Y)
    y2 = y - centerY
    x2 = x - centerX
    r = np.sqrt(x2**2+y2**2)
    return x2, y2, r

def Axis(dataWidth, dataHeight, m):
    x_ = np.linspace(0,dataWidth*m,dataWidth)
    y_ = np.linspace(0,dataHeight*m,dataHeight)
    return x_, y_

def SpatialGrid(x_, y_, centerX, centerY, dataWidth, dataHeight, m):
    #create spatial grid
    x, y = np.meshgrid(x_, y_)
    #centered grid
    x2 = x - dataWidth*m/2+centerX
    y2 = y - dataHeight*m/2+centerY
    r = np.sqrt(x2**2+y2**2)
    return x2, y2, r

def FreqGrid(x_, y_, l, f):
    #create frequency grid
    kx = np.fft.fftfreq(len(x_), np.diff(x_)[0]) 
    ky = np.fft.fftfreq(len(y_), np.diff(y_)[0])
    kxv, kyv = np.meshgrid(kx,ky)
    return np.fft.fftshift(kxv)*l*f, np.fft.fftshift(kyv)*l*f

def Phase(v_Kr, k, v_Ch, r, x2, y2):
    #phase mask
    return  k*np.arcsin(v_Kr/k)*r + v_Ch*np.arctan2(y2,x2)

def FourierField(phaseData, w, r):
    #field from mask
    Edata = np.exp(-w*r**2)*np.cos(phaseData)
    ft_Edata = np.fft.fft2(Edata)
    return abs(np.fft.fftshift(ft_Edata)+100*np.exp(-r**2/4E-4))**2

def AnaliticField(v_Ch, ri, wi, r, x2, y2):
    #field from formula
    return abs( np.cos(v_Ch*np.arctan2(y2,x2)+ pi/2*(v_Ch-1))*np.exp(-(r - ri)**2/wi**2) )**2

