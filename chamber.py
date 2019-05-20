from geometry import *
from constants import *
from numba import jit
import matplotlib.pyplot as plt
import numpy as np

class chamber:
    def __init__(self, idNumber, length, designAngle, designX, designY, actualAngle, actualX, actualY):
        self.id = idNumber
        self.length = length

        self.designAngle = designAngle
        self.designX = designX
        self.designY = designY
        self.designEndpoints = [[designX-length/2*math.cos(designAngle),designX+length/2*math.cos(designAngle)],[designY-length/2*math.sin(designAngle),designY+length/2*math.sin(designAngle)]]

        self.actualAngle = actualAngle
        self.actualX = actualX
        self.actualY = actualY
        self.actualEndpoints = [[actualX-length/2*math.cos(actualAngle),actualX+length/2*math.cos(actualAngle)],[actualY-length/2*math.sin(actualAngle),actualY+length/2*math.sin(actualAngle)]]

        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []
        self.alignStep  = [1,1,.5]

        self.fitness = []
        self.residualY = []




    def getResiduals(self, muonTrack, muonPath):
        #find predicted hit i.e. "track"

        interceptTrack = intersectAndHit(self.designEndpoints, muonTrack)

        #did it hit the chamber
        track =False
        minVal, maxVal = min(self.designEndpoints[1]), max(self.designEndpoints[1])
        if interceptTrack[1] < maxVal and interceptTrack[1] > minVal:
            track = True

        #find local dy/dx
        trackSlope = returnLocalDxDy(self.designAngle, muonTrack)
        transformedInterceptTrack = transformCord(self.designX, self.designY, self.designAngle, interceptTrack)
        #now, lets find the actual hit:
        hit = False
        for index, point in enumerate(muonPath[0]):
            if index == 0: continue
            segment = [[muonPath[0][index-1], muonPath[0][index]], [muonPath[1][index-1], muonPath[1][index]]]
            interceptHit  = intersectAndHit(self.actualEndpoints, segment)
            #did it hit the chamber
            minVal, maxVal = min(self.actualEndpoints[1]), max(self.actualEndpoints[1])
            if interceptHit[1] < maxVal and interceptHit[1] > minVal:
                hit = True
            if hit: 
                hitSlope = returnLocalDxDy(self.actualAngle, segment)
                transformedInterceptHit = transformCord(self.actualX, self.actualY, self.actualAngle, interceptHit)
                break

        if hit and track:
            self.hit[0].append(transformedInterceptHit[0])
            self.hit[1].append(transformedInterceptHit[1])
            self.hitXOverY.append(hitSlope)
            self.track[0].append(transformedInterceptTrack[0])
            self.track[1].append(transformedInterceptTrack[1])
            self.trackXOverY.append(trackSlope)

    def alignGradDescent(self, learningRates, stepSizes):
        hitY = np.asarray(self.hit[1])
        trackY = np.asarray(self.track[1])  
        dxdyTrack = np.asarray(self.trackXOverY)
        residualY = trackY-hitY
        possibleXDisplacements = [-stepSizes[0], 0, stepSizes[0]]
        possibleYDisplacements = [-stepSizes[1], 0, stepSizes[1]]
        possibleAngleDisplacements = [-stepSizes[2], 0, stepSizes[2]]



        #possibleXDisplacements = [0]

        minValue = 1000
        lowesState = [0,0,0]
        noDisValue = 0
        xSTD = []
        for xDis in possibleXDisplacements:
            for yDis in possibleYDisplacements:
                for angleDis in possibleAngleDisplacements:
                    predictedResidual =  yDis - dxdyTrack*xDis + hitY*dxdyTrack*angleDis
                    squaredDifference = np.power(predictedResidual - residualY,2)
                    squaredDifference = squaredDifference[~np.isnan(squaredDifference)]
                    stdDev = np.mean(squaredDifference)
                    if stdDev < minValue and not (xDis == 0 and yDis == 0 and angleDis ==0):
                        lowesState = [xDis,yDis, angleDis]
                        minValue  = stdDev
                    if xDis == 0 and yDis == 0 and angleDis ==0:
                        noDisValue = stdDev

        distance = math.sqrt(lowesState[0]*lowesState[0] + lowesState[1]*lowesState[1] + lowesState[2]*lowesState[2])
        slope = abs(minValue-noDisValue)/distance


        deltaX, deltaY, deltaAngle =  lowesState[0]*slope*learningRates[0], lowesState[1]*slope*learningRates[1], lowesState[2]*slope*learningRates[2]
        #slope = (xSTD[0] - xSTD[1])/2*stepSizes[0]
        #deltaX = slope*learningRates[0]
        #xDis = 0
        #angleDis = 0
        #print stdDev


        #deltaX, deltaY, deltaAngle = 0,0,0
        newX, newY, newAngle = deltaX, deltaY, deltaAngle
        print "design",  self.designX, self.designY, self.designAngle
        print "actual", self.actualX, self.actualY, self.actualAngle
        print "update", newX, newY, newAngle
        self.designAngle = self.designAngle + newAngle
        self.designX = self.designX + newX
        self.designY = self.designY + newY
        self.designEndpoints = [[ self.designX-self.length/2*math.cos( self.designAngle), self.designX+self.length/2*math.cos( self.designAngle)],[self.designY-self.length/2*math.sin( self.designAngle),self.designY+self.length/2*math.sin( self.designAngle)]]
        if abs(newX) < self.alignStep[0]/2:
            self.alignStep[0] = self.alignStep[0]/2
        if abs(newY) < self.alignStep[1]/2:
            self.alignStep[1] = self.alignStep[1]/2
        if abs(newAngle) < self.alignStep[2]/2:
            self.alignStep[2] = self.alignStep[2]/2

        self.fitness.append(stdDev)
        self.residualY = residualY


    def resetData(self):
        #print "design after align",  self.designX, self.designY, self.designAngle, self.designEndpoints
        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []



    def align(self):

        hitY = np.asarray(self.hit[1])
        trackY = np.asarray(self.track[1])  
        dxdyTrack = np.asarray(self.trackXOverY)
        residualY = trackY-hitY

        possibleXDisplacements = np.linspace(-self.alignStep[0],  self.alignStep[0], 10)
        possibleYDisplacements = np.linspace(-self.alignStep[1], self.alignStep[1], 10)
        possibleAngleDisplacements = np.linspace(-self.alignStep[2], self.alignStep[2], 10)

        #possibleYDisplacements = [0]
        #possibleXDisplacements = [0]
        #possibleAngleDisplacements=[0]
        #possibleXDisplacements = [-.01,.01]
        #possibleYDisplacements = [-.01,.01]
        #possibleAngleDisplacements = [-.01,.01]

        minValue = 100
        correctedPostion = [0,0,0]
        for xDis in possibleXDisplacements:
            for yDis in possibleYDisplacements:
                for angleDis in possibleAngleDisplacements:
                    predictedResidual =  yDis - dxdyTrack*xDis + hitY*dxdyTrack*angleDis
                    stdDev = np.mean(np.power(predictedResidual - residualY,2))
                    if minValue > stdDev:
                        minValue = stdDev
                        correctedPostion = [xDis, yDis, angleDis]
                    #print xDis, yDis, angleDis,stdDev  

        newX, newY, newAngle = correctedPostion[0], correctedPostion[1], correctedPostion[2] 
        print "design",  self.designX, self.designY, self.designAngle
        print "actual", self.actualX, self.actualY, self.actualAngle
        print "update", newX, newY, newAngle
        self.designAngle = self.designAngle + newAngle
        self.designX = self.designX + newX
        self.designY = self.designY + newY
        self.designEndpoints = [[ self.designX-self.length/2*math.cos( self.designAngle), self.designX+self.length/2*math.cos( self.designAngle)],[self.designY-self.length/2*math.sin( self.designAngle),self.designY+self.length/2*math.sin( self.designAngle)]]

        if abs(newX) < self.alignStep[0]/2:
            self.alignStep[0] = self.alignStep[0]/2
        if abs(newY) < self.alignStep[1]/2:
            self.alignStep[1] = self.alignStep[1]/2
        if abs(newAngle) < self.alignStep[2]/2:
            self.alignStep[2] = self.alignStep[2]/2

        print "design after align",  self.designX, self.designY, self.designAngle, self.designEndpoints
        self.hit = [[],[]]
        self.hitXOverY = []

        self.track = [[],[]]
        self.trackXOverY = []




    def plotChamber(self,sub1,sub2,sub3):
 
        self.designPlot = sub1.plot(self.designEndpoints[0],self.designEndpoints[1], color='blue', label="design Chamber Postition")
        self.actualPlot = sub1.plot(self.actualEndpoints[0],self.actualEndpoints[1], color='green', label="actual Chamber Postition")

        self.fitnessPlot = sub2.plot(self.fitness, color='black', label="fitness")
        self.residualPlot =  sub3.hist(self.residualY)

    def cleanChamberPlot(self):
        for plot in self.designPlot:
            plot.remove()
        for plot in self.actualPlot:
            plot.remove()
        for plot in self.fitnessPlot:
            plot.remove()

