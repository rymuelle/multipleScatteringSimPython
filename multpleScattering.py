from numba import jit
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import random


random.seed(1.0)

nEvents = 100000

xDistance = 100

yRange = [-100, 100]

typicalScatteringDistance = 10

angleConstant = 1.0

speedDecreaseConstant = .95

magneticField = 1.0

massOverCharge = 1.0

pi = 3.1415

verbose = 10

xBound = [0, 100]

yBound = [-100, 100]


def scatteringDistance():
    scatteringDistance =  typicalScatteringDistance/(10*random.random() )
    return scatteringDistance

def scatteringAngle(speed):
    sigma = angleConstant/(speed*100)
    deltaAngle = sigma*2*(.5-random.random())
    return deltaAngle

def scatteringSpeed(speed):
    speed = .95*speed
    return speed

#@jit
def iterateMuon(angleInitial, speed, charge, xInitial, yInitial):
    radiusOfCurvature = massOverCharge*speed/magneticField #negative means curve the other way

    #flip y by charge, then flip back
    yInitial = yInitial*charge

    x0 = xInitial - radiusOfCurvature*math.sin(angleInitial)
    y0 = yInitial + radiusOfCurvature*math.cos(angleInitial)

    #calculate scattering distance:
    distance = scatteringDistance()

    circumference = 2*pi*abs(radiusOfCurvature)

    if distance > circumference:
        distance = -999
        xFinal, yFinal, angleFinal = xInitial, yInitial, angleInitial
    else:
        angleCovered = distance/circumference*2*pi #angles are radians
        angleFinal = angleInitial + angleCovered + scatteringAngle(speed)

        xFinal = x0+radiusOfCurvature*math.sin(angleFinal)
        yFinal = y0-radiusOfCurvature*math.cos(angleFinal)

        speed = scatteringSpeed(speed)

    if xFinal < xInitial:
        distance = -999

    #flip y by charge, then flip back
    yFinal = yFinal*charge

    return xFinal, yFinal, angleFinal, speed, distance

def propagateMuon(angleInitial, speed, charge, xInitial, yInitial):
    for i in range(100):
        xInitial, yInitial, angleInitial, speed, distance = iterateMuon(angleInitial, speed, charge, xInitial, yInitial)

        if verbose > 9: print angleInitial, "\t", speed, "\t", charge, "\t", xInitial, "\t", yInitial

        if distance == -999:
            break

        if xBound[0] > xInitial or xBound[1] < xInitial:
            break

        if yBound[0] > yInitial or yBound[1] < yInitial:
            break

    if verbose > 9: print "end loop"



 


y = []
for i in range(nEvents):
    angle = 0
    speed = 1000

    charge = random.random()
    if charge > .5: charge = 1
    else: charge = -1

    xInitial = 0
    yInitial = 0
    if verbose > 9: print "start ", angle, speed, charge, xInitial, yInitial
    hitLocation = propagateMuon(angle, speed, charge, xInitial, yInitial)
    #if hitLocation != -999: y.append(hitLocation)


#n, bins, patches = plt.hist(y, 50, density=True, facecolor='g', alpha=0.75,range=[-10, 10])
#
#
#plt.xlabel('y position')
#plt.ylabel('Probability')
#plt.title('Histogram of hit locations')
##plt.show()
#plt.savefig("output/hit_position_hist.png")