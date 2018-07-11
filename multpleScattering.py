from numba import jit
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import random


random.seed(1.0)

nEvents = 10000

xDistance = 100

yRange = [-100, 100]

typicalScatteringDistance = 10

angleConstant = 4

speedDecreaseConstant = .95

magneticField = .2

massOverCharge = 1.0

pi = 3.1415

verbose = 5

xBound = [0, 100]

yBound = [-100, 100]

@jit
def scatteringDistance():
    scatteringDistance =  typicalScatteringDistance/(10*random.random() )
    return scatteringDistance

@jit
def scatteringAngle(speed):
    sigma = angleConstant/(speed)
    deltaAngle = sigma*2*(.5-random.random())
    return deltaAngle

@jit
def scatteringSpeed(speed,angle):
    speed = speedDecreaseConstant*speed*math.cos(angle)
    return speed

#@jit
def circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial):
    x0 = xInitial - radiusOfCurvature*math.sin(angleInitial)
    y0 = yInitial + radiusOfCurvature*math.cos(angleInitial)
    return x0, y0

@jit
def returnRadiusOfCurvature(massOverCharge, speed, magneticField):
    radiusOfCurvature = massOverCharge*speed/magneticField
    return radiusOfCurvature

@jit
def iterateMuon(angleInitial, speed, charge, xInitial, yInitial):
    #radiusOfCurvature = massOverCharge*speed/magneticField #negative means curve the other way
    radiusOfCurvature = returnRadiusOfCurvature(massOverCharge, speed, magneticField)

    #flip y by charge, then flip back
    yInitial = yInitial*charge

    x0, y0 = circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial)

    #calculate scattering distance:
    distance = scatteringDistance()

    circumference = 2*pi*abs(radiusOfCurvature)

    if distance > circumference:
        distance = -999
        xFinal, yFinal, angleFinal = xInitial, yInitial, angleInitial
        angleAfterScatter = angleInitial
    else:
        angleCovered = distance/circumference*2*pi #angles are radians
        angleFinal = angleInitial + angleCovered

        xFinal, yFinal = circleFromPointAndRadius(x0,y0, -radiusOfCurvature, angleFinal)

        scatAngle = scatteringAngle(speed)
        angleAfterScatter =  angleFinal + scatAngle

        speed = scatteringSpeed(speed,scatAngle)

    if xFinal < xInitial:
        distance = -999

    #flip y by charge, then flip back
    yFinal = yFinal*charge

    return xFinal, yFinal, angleAfterScatter, speed, distance, x0, y0, radiusOfCurvature

@jit
def circleIntersectLine(x0,y0,x1,y1, xCircle, yCircle, radiusOfCurvature, charge):

    # x = my +b
    m = (x1-x0)/(y1-y0)
    bInt = x0 - m*y0 

    rSquared = radiusOfCurvature*radiusOfCurvature

    a = (1+m*m)
    b = 2*((bInt-xCircle)*m-yCircle)
    c = (bInt-xCircle)*(bInt-xCircle)+yCircle*yCircle-rSquared

    #sqrtValue = -b*b - 2*b*m*yCircle + 2*b*xCircle + m*m*rSquared - m*m*yCircle*yCircle + 2*m*yCircle*xCircle + rSquared - xCircle*xCircle
    sqrtValue = b*b-4*a*c

    if sqrtValue > 0:
        yIntercept1 = (-b-math.sqrt(sqrtValue))/(2*a)
        xIntercept1 = m*yIntercept1 + bInt
    else:
        yIntercept1 = -999
        xIntercept1 = -999

    if verbose > 9: print "intercept ", xIntercept1, yIntercept1*charge

    return yIntercept1*charge

#@jit
def propagateMuon(angleInitial, speed, charge, xInitial, yInitial):
    for i in range(100):

        if i == 0:
            radiusOfCurvature = returnRadiusOfCurvature(massOverCharge, speed, magneticField)
            x0 , y0 = circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial)
            yTrackOut = circleIntersectLine(100, 0, 100, 100, x0, y0, radiusOfCurvature, charge)

        xInitial, yInitial, angleInitial, speed, distance, x0, y0, radiusOfCurvature = iterateMuon(angleInitial, speed, charge, xInitial, yInitial)

        #if verbose > 9: print angleInitial, "\t", speed, "\t", charge, "\t", xInitial, "\t", yInitial, "\t",  x0, "\t", y0, "\t", radiusOfCurvature
        if verbose > 5: print "angle {} speed {} charge {} x {} y {} radius {}".format(angleInitial, speed, charge, xInitial, yInitial,  x0, y0, radiusOfCurvature)

        yHitOut = circleIntersectLine(100, 0, 100, 100, x0, y0, radiusOfCurvature, charge)

        if distance == -999:
            break

        if xBound[0] > xInitial or xBound[1] < xInitial:
            break

        if yBound[0] > yInitial or yBound[1] < yInitial:
            break
        
    if verbose > 5: 
        print "end loop yhitOut {}, yTrackOut {}".format(yHitOut, yTrackOut)



    residualLeavingBounds = yTrackOut -  yHitOut
    if verbose > 5: print "residual leaving bounds ", residualLeavingBounds

    return residualLeavingBounds



 

residualLeavingBounds = []

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
    residual = propagateMuon(angle, speed, charge, xInitial, yInitial)
    residualLeavingBounds.append(residual)
    #if hitLocation != -999: y.append(hitLocation)


n, bins, patches = plt.hist(residualLeavingBounds, 50, density=True, facecolor='g', alpha=0.75,range=[-10, 10])


plt.xlabel('y residual')
plt.ylabel('Probability')
plt.title('Histogram of residual locations')
#plt.show()
plt.savefig("output/hist_residual.png")