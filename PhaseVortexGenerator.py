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
from vortex_generator_2 import Phase, PhaseMatrix

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
m = 8E-4           #pixel size in sm
dataWidth = slm.width_px
dataHeight = slm.height_px

f_s = 50.0 
l_s = 1.55E-4
#d = 1E10 #distance sm

#vortex parameters
ri = 1.0        #vortex radius
wi = 0.1      #ring width
v_Ch = 2.0      #vortex charge
centerX = 0.0/m   #Vortex center
centerY = 0.0/m   

#scaling
f = f_s/m            
l = l_s/m  

v_r =  ri/m                
v_w = wi/m               

k = 2*pi/l                         #tot-Wave vector
v_Kr = k*v_r/f                     #r-Wave vector
w = (k**2 * v_w**2) / (16 * f**2)  #Vortex width    

dataWidth = slm.width_px
dataHeight = slm.height_px

x2, y2, r = PhaseMatrix(dataWidth, dataHeight, centerX, centerY)
raw_Phase = Phase(v_Kr, v_Ch, r, x2, y2)

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
