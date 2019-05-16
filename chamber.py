from geometry import *
from constants import *
from numba import jit
import matplotlib.pyplot as plt

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

        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []




    def getResiduals(self, muonTrack, muonPath):
        #find predicted hit i.e. "track"
        interceptTrack, track = intersectAndHit(self.knownEndpoints, muonTrack)
        #find local dy/dx
        trackSlope= returnLocalDxDy(self.knownAngle, muonTrack)

        #now, lets find the real hit:
        for index, point in enumerate(muonPath[0]):
            if index == 0: continue
            segment = [[muonPath[0][index-1], muonPath[0][index]], [muonPath[1][index-1], muonPath[1][index]]]
            interceptHit, hit = intersectAndHit(self.realEndpoints, segment)
            if hit: 
                hitSlope = returnLocalDxDy(self.realAngle, segment)
                break

        if hit and track:
            self.hit[0].append(interceptHit[0])
            self.hit[1].append(interceptHit[1])
            self.hitXOverY.append(hitSlope)
            self.track[0].append(interceptTrack[0])
            self.track[1].append(interceptTrack[1])
            self.trackXOverY.append(trackSlope)




    def plotChamber(self):
        plt.plot(self.knownEndpoints[0],self.knownEndpoints[1], color='blue', label="known Chamber Postition")
        plt.plot(self.realEndpoints[0],self.realEndpoints[1], color='green', label="real Chamber Postition")
