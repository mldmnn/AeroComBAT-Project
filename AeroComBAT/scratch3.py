# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:03:21 2016

@author: Ben
"""
import sys
import os
sys.path.append(os.path.abspath('..'))

# =============================================================================
# HEPHAESTUS VALIDATION 8 - BEAM DISPLACEMENTS AND ROTATIONS SIMPLE AL BOX BEAM
# =============================================================================

# IMPORTS:
import numpy as np
from AeroComBAT.Structures import MaterialLib
from AeroComBAT.AircraftParts import Wing
from AeroComBAT.FEM import Model

# Define the width of the cross-section
c = .076
ctip = 0.0076+.002
croot = 0.0076+.002
x1 = -0.04/croot/2
x2 = 0.04/croot/2
span = .305
p1 = np.array([c/2,0.,0.])
p2 = np.array([c/2,span,0.])
Y_rib = np.linspace(0.,1.,2)
b_s = np.linalg.norm((Y_rib[0],Y_rib[-1]))

matLib = MaterialLib()
matLib.addMat(1,'AL','iso',[68.9e9,.33,27000],.0005)
matLib.addMat(2,'Weak_mat','iso',[100,.33,10],.0005)
matLib.addMat(3,'AS43501-6*','trans_iso',[142e9,9.8e9,.34,.42,6e9,20000],0.0005)

n_ply = [4,4,4,4]
m_ply = [3,3,3,3]
th_ply = [30,-30,-30,30]
#n_ply = [4]
#m_ply = [1]

n_orients = 1
n_lams = 4
typeXSect = 'rectBox'
noe_dens = 120
chordVec=np.array([-1.,0.,0.])


# For tension bending coupling
#m_ply = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#th_ply = [0,0,0,0,-30,-30,-30,-30,0,0,0,0,30,30,30,30]


wing1 = Wing(1,p1,p2,croot,ctip,x1,x2,Y_rib,n_ply,m_ply,matLib,name='box',\
    noe=noe_dens,chordVec=chordVec,ref_ax='shearCntr',n_orients=n_orients,\
    n_lams=n_lams,typeXSect=typeXSect,meshSize=1,th_ply=th_ply)
sbeam1 = wing1.wingSects[0].SuperBeams[0]


x1 = np.array([0,0.,0.])
x2 = np.array([c,0.,0.])
x3 = np.array([c,span,0.])
x4 = np.array([0,span,0.])
nspan = 36
nchord = 2*5

wing1.addLiftingSurface(1,x1,x2,x3,x4,nspan,nchord)

# Make a FEM model
model  = Model()

model.addAircraftParts([wing1])

# Apply the constraint for the model
model.applyConstraints(0,'fix')
model.plotRigidModel(numXSects=10)

model.normalModesAnalysis()
freqs = model.freqs
'''
# Aerodynamic Model Validation
model.calcAIC(.24,.47,.4572/2,symxz=True)

model.normalModesAnalysis()

pbar = np.dot(np.linalg.inv(model.D),np.dot(model.W,-model.umode[:,0]/max(abs(model.umode[:,0]))))
pbarReal = np.real(pbar)
pbarImag = np.imag(pbar)

pbarPlot = pbar[330:330+10]
#pbarPlot = pbar[0:0+10]

xs = np.zeros((10))
for i in range(0,10):
    xs[i] = model.aeroBox[i].Xr[0]
xs = xs/c

import matplotlib.pyplot as plt
plt.figure(1)
plt.hold(True)
plt.plot(xs,np.real(pbarPlot),label='real part')
plt.plot(xs,np.imag(pbarPlot),label='imaginary part')
plt.legend()
plt.grid(True)
plt.hold(False)
'''
'''
# CASE 1:
# Apply the case load
model.resetPointLoads()
tipLoad = np.array([10000.,0.,0.,0.,0.,0.])
F = {80:tipLoad}
model.applyLoads(1,F=F)
# Run the analysis
model.staticAnalysis(1)
model.plotDeformedModel(figName='V8 Case 1',numXSects=8,contLim=[-4.0e6,4.0e6],\
    warpScale=100,displScale=10,contour='sig_33')
'''

U_vec = np.linspace(1,1000,100)
kr_vec = np.array([.0001,.001,.01,.05,.1,.5,1.,5.,10.,50.])*10
M_vec = [0.]*len(kr_vec)
rho_0 = 1.225
nmodes = 6

model.jitflutterAnalysis(U_vec,kr_vec,M_vec,c,rho_0,nmodes,symxz=True)

# flutter plots
import matplotlib.pyplot as plt
plt.figure(1)
plt.hold(True)
for PID, point in model.flutterPoints.iteritems():
    plt.plot(U_vec,point.gamma,label='mode'+str(PID))
plt.legend(loc=3)
#plt.ylim([-.001,150])
plt.grid(True)
plt.hold(False)

plt.figure(2)
plt.hold(True)
for PID, point in model.flutterPoints.iteritems():
    plt.plot(U_vec,point.omega,label='mode'+str(PID))
plt.legend(loc=1)
#plt.ylim([0,150])
plt.grid(True)
plt.hold(False)
'''
import cProfile
#cProfile.run('model.flutterAnalysis(U_vec,kr_vec,M_vec,c/2,rho_0,nmodes,symxz=True,g=.01)')
flatPlateFlutter = np.genfromtxt('FlatPlateFlutterResults.csv', delimiter=',',dtype=float)
plt.figure(3)
plt.hold(True)
for i in range(0,3):
    plt.plot(flatPlateFlutter[1:,0],flatPlateFlutter[1:,i+1],label='mode'+str(i+1))
plt.legend(loc=3)
#plt.ylim([-.001,150])
plt.grid(True)
plt.hold(False)

plt.figure(4)
plt.hold(True)
for i in range(0,3):
    plt.plot(flatPlateFlutter[1:,0],flatPlateFlutter[1:,i+4],label='mode'+str(i+1))
plt.legend(loc=1)
#plt.ylim([0,150])
plt.grid(True)
plt.hold(False)
'''
'''
model.normalModesAnalysis()
model.plotDeformedModel(mode=1,figName='mode 1',numXSects=10,displScale=1)
model.plotDeformedModel(mode=2,figName='mode 2',numXSects=10,displScale=1)
model.plotDeformedModel(mode=3,figName='mode 3',numXSects=10,displScale=1)
model.plotDeformedModel(mode=4,figName='mode 4',numXSects=10,displScale=1)
model.plotDeformedModel(mode=5,figName='mode 5',numXSects=10,displScale=1)
'''
'''
import cProfile
# Initialize an array of PANIDs
PANIDs = model.aeroBox.keys()
# Initialize the number of panels
numPan = len(PANIDs)
Area = np.zeros((numPan,numPan))
# For all the recieving panels
for i in range(0,numPan):
    recievingBox = model.aeroBox[PANIDs[i]]
    Area[i,i] = recievingBox.Area
model.AeroArea = Area
cProfile.run('model.calcAIC(0.,1.,0.8990566037735849*2)')
'''
'''
# Test Normal modes
model.normalModesAnalysis(analysis_name='Normal_Modes')
# Write the beam displacements and rotations to a file
freqs = model.freqs
model.plotDeformedModel(mode=1,figName='Mode 1',analysis_name='Normal_Modes',\
    numXSects=10,warpScale=1,displScale=2)
model.plotDeformedModel(mode=2,figName='Modes 2',analysis_name='Normal_Modes',\
    numXSects=10,warpScale=1,displScale=2)
model.plotDeformedModel(mode=3,figName='Modes 3',analysis_name='Normal_Modes',\
    numXSects=10,warpScale=1,displScale=2)
model.plotDeformedModel(mode=4,figName='Modes 4',analysis_name='Normal_Modes',\
    numXSects=10,warpScale=1,displScale=2)
model.plotDeformedModel(mode=5,figName='Modes 5',analysis_name='Normal_Modes',\
    numXSects=10,warpScale=1,displScale=2)
model.plotDeformedModel(mode=6,figName='Modes 6',analysis_name='Normal_Modes',\
    numXSects=10,warpScale=1,displScale=2)
'''
'''
# CASE 2:
# Apply the case load
def f(x):
    vx = -0.1*(-1.0e3*x[2]**2+6e7*x[2]+1.0e6)
    vy = (-1.0e3*x[2]**2+6e7*x[2]+1.0e6)
    pz = 0
    tz = .2*c*(-1.0e3*x[2]**2+6e7*x[2]+1.0e6)
    return np.array([vx,vy,pz,tz])/1.0e5
wing1.applyLoads(f=f,allElems=True)
# Run the analysis
wing1.staticAnalysis(resetPointLoads=True)
wing1.plotDeformedWing(figName='V8 Case 2',numXSects=10,contLim=[0.,5.0e8],\
    warpScale=10,displScale=10,contour='MaxPrin')
# Write the beam displacements and rotations to a file
sbeam1.writeDisplacements(fileName = 'V8_Case_2.csv')

# CASE 3:
# Apply the case load
def f(x):
    vx = 1e3
    vy = 1e3
    pz = -1e3
    tz = 1e3
    return np.array([vx,vy,pz,tz])/1e1
wing1.applyLoads(f=f,allElems=True)
# Run the analysis
wing1.staticAnalysis(resetPointLoads=True)
wing1.plotDeformedWing(figName='V8 Case 3',numXSects=10,contLim=[0.,5.0e8],\
    warpScale=100,displScale=10,contour='MaxPrin')
# Write the beam displacements and rotations to a file
sbeam1.writeDisplacements(fileName = 'V8_Case_3.csv')'''