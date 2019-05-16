from numba import jit
from geometry import scatteringDistance, scatteringAngle
from constants import *
from iterateMuon import iterateMuon
from circleIntersectLine import circleIntersectLine
import math

xBound = [0, 100]

yBound = [-1000, 1000]

#@jit
def propagateMuon(angleInitial, speed, charge, xInitial, yInitial):
    angleInitial, speed, charge, xInitial, yInitial = angleInitial+.0, speed+.0, charge+.0, xInitial+.0, yInitial+.0
    
    #make ieal track
    try:
        slopeInital = math.atan(angleInitial)
    except:
        print "bad angle"
        return []

    xTrackFinal, yTrackFinal = xBound[1], xBound[1]*slopeInital + yInitial

    muonTrack = [[xInitial,xTrackFinal],[yInitial,yTrackFinal]]

    #simulate multiple scattering
    xPositions = [xInitial]
    yPositions = [yInitial]
    currentAngle = angleInitial

    while xPositions[-1] < xBound[1]:
        pathLength = scatteringDistance()
        deltaAngle = scatteringAngle(speed)

        nextXPosition = xPositions[-1]+math.cos(currentAngle)*pathLength
        nextYPosition = yPositions[-1]+math.sin(currentAngle)*pathLength

        if nextXPosition > xBound[1]:
            pathLength = (xBound[1]-xPositions[-1])/math.cos(currentAngle)
            nextXPosition = xBound[1]
            nextYPosition = yPositions[-1]+math.sin(currentAngle)*pathLength

        xPositions.append(nextXPosition)
        yPositions.append(nextYPosition)

        currentAngle = currentAngle + deltaAngle

    return muonTrack, [xPositions, yPositions]