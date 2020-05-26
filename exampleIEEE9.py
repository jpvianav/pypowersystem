# Containers
from System import System
from DAE import DAE

#Solvers
from methods import cSimulation
from methods import dSimulation

#testSystem
from testSystem import ieee9

from numpy import r_
from numpy import zeros
from numpy import nonzero
from numpy import savetxt
import numpy as np 

import time

# Control!
from control import svrSA

# Graphs!
import matplotlib.pyplot as plt

# -----------------------------------------------------
# Events
# -----------------------------------------------------
def anEvent(tEvent, System , DAE, t, dt):
    if tEvent-dt < t and t < tEvent + dt:
        # System.load.p[0] = 1.0
        System.lne.status[4] = 0
        flagEvent = True
    else:
        flagEvent = False
    return flagEvent
        
if __name__ == '__main__':
    #Load test system
    system, dae = ieee9()
      
    # Dynamic simulation!!!!
    tMax = 5 #(s)
    dT = 100e-3 #(s)
    tEvent = 1
    event = lambda t, dtMin:  anEvent(tEvent, system, dae, t, dtMin)
    t1 = time.time()
    # Simulation using trapezoidal method
    cSimulation(system, dae, tMax = tMax, dT = dT,  iterMax = 10, tol = 1e-4, event = event)
    
    # Simulation using a linearized version of the system 
    # dSimulation(system, dae, tMax = tMax, dT = dT,  event = event)
    print('\n Elapsed time: '+str(time.time()- t1))

    # ======================================================================
    # Graphs
    # Variables of interest
    idxqh = system.syn4.qh
    idxvm = system.bus.vm
    idxAVR = system.ieee1.vref
    fig, axs = plt.subplots(3,1)
    #Voltages
    axs[0].plot(dae.tOut, dae.yOut[:,idxvm])
    #Angle
    axs[1].plot(dae.tOut, dae.xOut[:,0])
    #Speed
    axs[2].plot(dae.tOut, dae.xOut[:,1])



    plt.show()




