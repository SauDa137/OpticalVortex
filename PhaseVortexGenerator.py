# -*- coding: utf-8 -*-

#--------------------------------------------------------------------#
#                                                                    #
# Copyright (C) 2020 HOLOEYE Photonics AG. All rights reserved.      #
# Contact: https://holoeye.com/contact/                              #
#                                                                    #
# This file is part of HOLOEYE SLM Display SDK.                      #
#                                                                    #
# You may use this file under the terms and conditions of the        #
# "HOLOEYE SLM Display SDK Standard License v1.0" license agreement. #
#                                                                    #
#--------------------------------------------------------------------#


# Calculates an axicon and shows it on the SLM.

import math
from os import X_OK
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from vortex_generator_2 import CreatSpatialAxis, CreateSpatialGrid, BesselVortexMask

# Import the SLM Display SDK:
import detect_heds_module_path
from holoeye import slmdisplaysdk

# Initializes the SLM library
slm = slmdisplaysdk.SLMInstance()

# Check if the library implements the required version
if not slm.requiresVersion(3):
    exit(1)

# Detect SLMs and open a window on the selected SLM
#error = slm.open()
#assert error == slmdisplaysdk.ErrorCode.NoError, slm.errorString(error)

# Open the SLM preview window in "Fit" mode:
# Please adapt the file showSLMPreview.py if preview window
# is not at the right position or even not visible.
from showSLMPreview import showSLMPreview
showSLMPreview(slm, scale=0.0)

#setup parameters
PixelSize = 8E-4           #pixel size in sm
dataWidth = slm.width_px
dataHeight = slm.height_px

lenseFocalDistance = 50.0 
waveLength = 1.55E-4
#d = 1E10 #distance sm

#vortex parameters
vortexRadius = 1.0        #vortex radius
vortexWidth = 0.1      #ring width
vortexCharge = 2.0      #vortex charge
centerX = 0.0/PixelSize   #Vortex center
centerY = 0.0/PixelSize   

#scaling
lenseFocalDistanceScaled = lenseFocalDistance/PixelSize            
waveLengthScaled = waveLength/PixelSize  

vortexRadiusScaled =  vortexRadius/PixelSize                
vortexWidthScaled = vortexWidth/PixelSize               

vortexWaveVector = 2*pi/waveLengthScaled                         #tot-Wave vector
vortexWaveVectorRadial = vortexWaveVector*vortexRadiusScaled/lenseFocalDistanceScaled                     #r-Wave vector
w = (vortexWaveVector**2 * vortexWidthScaled**2) / (16 * lenseFocalDistanceScaled**2)  #Vortex width    

dataWidth = slm.width_px
dataHeight = slm.height_px
x_axis, y_axis = CreatSpatialAxis(dataWidth, dataHeight, PixelSize)
x_grid_centered, y_grid_centered, r = CreateSpatialGrid(x_axis, y_axis, centerX, centerY, dataWidth, dataHeight, PixelSize)
raw_Phase = BesselVortexMask(vortexWaveVectorRadial, vortexWaveVector, vortexCharge, r, x_grid_centered, y_grid_centered)

# Reserve memory for the phase data matrix.
# Use data type single to optimize performance:
phaseData = slmdisplaysdk.createFieldSingle(dataWidth, dataHeight)

for y in range(dataHeight):
    row = phaseData[y]
    for x in range(dataWidth):
        row[x] = raw_Phase[y][x]

# Show data on the SLM:
error = slm.showPhasevalues(phaseData)
assert error == slmdisplaysdk.ErrorCode.NoError, slm.errorString(error)

# If your IDE terminates the python interpreter process after the script is finished, the SLM content
# will be lost as soon as the script finishes.

# You may insert further code here.

# Wait until the SLM process is closed:
print("Waiting for SDK process to close. Please close the tray icon to continue ...")
error = slm.utilsWaitUntilClosed()
assert error == slmdisplaysdk.ErrorCode.NoError, slm.errorString(error)

# Unloading the SDK may or may not be required depending on your IDE:
slm = None
