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

random.seed(1.0)

residualLeavingBounds = []

'''
class chamber:
    def __init__(self, idNumber, length, knownAngle, knownX, knownY, realAngle, realX, realY):
        self.id = idNumber
        self.length = length

        self.knownAngle = knownAngle
        self.knownX = knownX
        self.knownY = knownY

        self.realAngle = realAngle
        self.realX = realX
        self.realY = realY

        self.hitX = []
        self.hitY = []
        self.hitXOverY = []

        self.trackX = []
        self.trackY = []
        self.trackXOverY = []

    def getTrack(self,)

'''



y = []
for i in range(nEvents):

    if i%1000==0: print i*1.0/nEvents
    angle = 0
    speed = 1000

    charge = random.random()
    if charge > .5: charge = 1
    else: charge = -1

    xInitial = 0
    yInitial = 0
    if verbose > 5: print "start  angle {} speed {} charge {} x {} y {}".format( angle, speed, charge, xInitial, yInitial)
    yTrackOut, yHitOut, angleTrack = propagateMuon(angle, speed, charge, xInitial, yInitial)
    residual =  yTrackOut, yHitOut
    residualLeavingBounds.append(residual)
    #if hitLocation != -999: y.append(hitLocation)

'''
n, bins, patches = plt.hist(residualLeavingBounds, 50, density=True, facecolor='g', alpha=0.75,range=[-10, 10])


plt.xlabel('y residual')
plt.ylabel('Probability')
plt.title('Histogram of residual locations')
plt.show()
plt.savefig("output/hist_residual.png")
'''