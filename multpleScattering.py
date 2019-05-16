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

@jit
def segmentToSlopeIntercept(segment):
    if (segment[0][0] - segment[0][1] != 0):
        slope = (segment[1][0] - segment[1][1])/(segment[0][0] - segment[0][1])
        intercept = segment[1][0] - slope*segment[0][0]
    else:
        slope, intercept = float('nan'),float('nan')
    return slope, intercept

#@jit
def returnIntersection(segment0, segment1):
    m0, b0 = segmentToSlopeIntercept(segment0)
    m1, b1 = segmentToSlopeIntercept(segment1)
  
    #what if the slopes are the same?
    if m0 == m1:
        print "same slope"
        if b0 == b1: intersect = True
        return float('nan'),float('nan'),intersect

    #what if one line is verticle?
    print "slopes", m0, m1
    print "intercepts", b0, b1
    if math.isnan(m0):
        x =  segment0[0][0]
    if math.isnan(m1) and x:
        print "no x intercept"
        return float('nan'),float('nan'),intersect
    elif math.isnan(m1):
        x =  segment1[0][0]

    #ok, if both are not verticle, find x
    if  'x' not in locals():
        x = (b0-b1)/(m1-m0)
    # find y
    if not math.isnan(m0):
        y = m0*x+b0
    else:
        y = m1*x+b1
    print x, y


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False


class chamber:
    def __init__(self, idNumber, length, knownAngle, knownX, knownY, realAngle, realX, realY):
        self.id = idNumber
        self.length = length

        self.knownAngle = knownAngle
        self.knownX = knownX
        self.knownY = knownY
        self.knownEndpoints = [[knownX-length/2*math.cos(knownAngle),knownX+length/2*math.cos(knownAngle)],[knownY-length/2*math.sin(knownAngle),knownY+length/2*math.sin(knownAngle)]]

        self.realAngle = realAngle
        self.realX = realX
        self.realY = realY
        self.realEndpoints = [[realX-length/2*math.cos(realAngle),realX+length/2*math.cos(realAngle)],[realY-length/2*math.sin(realAngle),realY+length/2*math.sin(realAngle)]]

        self.hitX = []
        self.hitY = []
        self.hitXOverY = []

        self.trackX = []
        self.trackY = []
        self.trackXOverY = []

    def getResiduals(self, muonTrack, muonPath):
        #find predicted hit i.e. "track"
        returnIntersection(muonTrack,  self.realEndpoints)
        L1 = line([self.realEndpoints[0][0],self.realEndpoints[1][0]], [self.realEndpoints[0][1],self.realEndpoints[1][1]])
        L2 = line([muonTrack[0][0],muonTrack[1][0]], [muonTrack[0][1],muonTrack[1][1]])
        R = intersection(L1, L2)
        if R:
            print "Intersection detected:", R
        else:
            print "No single intersection point detected"


    def plotChamber(self):
        plt.plot(self.knownEndpoints[0],self.knownEndpoints[1], color='blue', label="known Chamber Postition")
        plt.plot(self.realEndpoints[0],self.realEndpoints[1], color='green', label="real Chamber Postition")


chamber1 = chamber(1, 100, math.pi/2, 50, 0, 3.1415/2 +.1, 45, 0)



for i in range(nEvents):

    if i%1000==0: print i*1.0/nEvents


    #set up inital state of muon
    angleInitial = .1
    speedInitial = 1000

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
    plt.plot(muonTrack[0],muonTrack[1], color='orange', label="track")
    plt.plot(muonPath[0],muonPath[1], marker = 'o', color='red', label="actual path")
    chamber1.plotChamber()
    plt.legend()
    plt.show()
    plt.clf()
