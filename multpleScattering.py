from numba import jit
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import random
from geometry import *
from constants import *
from iterateMuon import iterateMuon
from circleIntersectLine import circleIntersectLine
from propagateMuon import propagateMuon
from chamber import chamber
import numpy as np
import pickle
random.seed(1.0)

residualLeavingBounds = []


sub1 = plt.subplot(212)
sub1.margins(0.05)           # Default margin is 0.05, value 0 means fit
sub1.set_xlim([0, 100])
sub1.set_ylim([-200, 200])

sub2 = plt.subplot(221) 
sub2.set_title('Fitness')
sub2.set_xlim([0, 40])

sub3 = plt.subplot(222)
sub3.set_title('y Residual')

#plt.show()


#sub1 = plt.subplot(212)
#sub1.set_xlim([0, 100])
#sub1.set_ylim([-100, 100])
##sub1.axis([0, 100, -100, 100])
#sub2 = plt.subplot(221)
#sub2.set_xlim([0, 40])
#sub3 = plt.subplot(222)
#sub3.set_xlim([-10, 10])
#sub2.plot([0,1])


designLength, designPhi, designX, designY = 100, math.pi/2, 50, 0
deltaPhi, deltaX, deltaY = .01,5,0
#eltaPhi, deltaX, deltaY = .1,-2,1
chamber1 = chamber(1, designLength, designPhi, designX, designY, designPhi+deltaPhi, designX+deltaX, designY+deltaY)
chamber1.plotChamber(sub1,sub2,sub3)


def shootMuons(chamber1):
    for i in range(nEvents):
    
        if i%1000==0: print i*1.0/nEvents
    
        #set up inital state of muon
        angleInitial = 1
        speedInitial = 1000
    
        angleInitial = random.random()-.5
    
        charge = random.random()
        if charge > .5: charge = 1
        else: charge = -1
    
        xInitial = 0
        yInitial = 0
    
        #create muon track
        if verbose > 5: print "start  angle {} speed {} charge {} x {} y {}".format( angleInitial, speedInitial, charge, xInitial, yInitial)
        muonTrack, muonPath = propagateMuon(angleInitial, speedInitial, charge, xInitial, yInitial)
    
        chamber1.getResiduals(muonTrack, muonPath)
    
        # note the y and x axis are not to scale, meaning things are stretched. A tilted chamber will look shorter
        if i%10000==0:
            #plt.clf()
            trackPaths = sub1.plot(muonTrack[0],muonTrack[1], color='orange', label="track")
            muonPaths = sub1.plot(muonPath[0],muonPath[1], marker = 'o', color='red', label="actual path")
            legend = sub1.legend()
            plt.pause(0.001)
            for muonPath in muonPaths:
                muonPath.remove()
            for trackPath in trackPaths:
                trackPath.remove()
           #plt.show()
            #plt.draw()
            #plt.clf()


learningRates = [50,10,1.5]
stepSizes = [.01,.01,.01]
for i in range(400):


    shootMuons(chamber1)

    #chamber1.alignGradDescent(learningRates, stepSizes)

    chamber1.align()
    #chamber1.align()
    chamber1.resetData()

    chamber1.cleanChamberPlot()
    chamber1.plotChamber(sub1,sub2,sub3)



'''
xResidual = np.subtract( chamber1.hit[1], chamber1.track[1])
dxdyResidual = np.subtract( chamber1.hitXOverY, chamber1.trackXOverY)


plt.hist(xResidual)
plt.show()

plt.hist(dxdyResidual)
plt.show()

plt.scatter(xResidual,dxdyResidual, alpha=.1)
plt.show()
'''
#output = {"length":designLength, "xDesign":chamber1.designX, "yDesign":chamber1.designY, "angleDesign":chamber1.designAngle, "xActual":chamber1.actualX, "yActual":chamber1.actualY, "angleActual":chamber1.actualAngle, "yHit": chamber1.hit[1], "yTrack":chamber1.track[1], "dxdyHit": chamber1.hitXOverY, "dxdyTrack":chamber1.trackXOverY}
#
#with open("output/chamber_residuals_nEvent_{}_des_{}_{}_{}_actual_{}_{}_{}.pickle".format(nEvents,chamber1.designX,chamber1.designY,chamber1.designAngle,chamber1.actualX,chamber1.actualY,chamber1.actualAngle), 'wb') as f:
#    pickle.dump(output, f)

