import math
import random
from numba import jit
from constants import *


#b = c
#p = yCircle
#q = xCircle


#@jit
def circleIntersectLine(x0,y0,x1,y1, xCircle, yCircle, radiusOfCurvature, charge):

    x0,y0,x1,y1, xCircle, yCircle, radiusOfCurvature, charge = x0+.0, y0+.0, x1+.0, y1+.0, xCircle+.0, yCircle+.0, radiusOfCurvature+.0, charge+.0

    # x = my +b
    m = (x1-x0)/(y1-y0)
    bInt = (x0) - m*(y0) 
    if charge < 0:
        m = -m

    rSquared = radiusOfCurvature*radiusOfCurvature


    a = (1+m*m)
    b = 2*((bInt-xCircle)*m-yCircle)


    c = (bInt-xCircle)*(bInt-xCircle)+yCircle*yCircle-rSquared

    c = (xCircle*xCircle - rSquared + yCircle*yCircle - 2*bInt*xCircle + bInt*bInt)

    #sqrtValue = -b*b - 2*b*m*yCircle + 2*b*xCircle + m*m*rSquared - m*m*yCircle*yCircle + 2*m*yCircle*xCircle + rSquared - xCircle*xCircle

    sqrtValue  = b*b-4*a*c

    if sqrtValue > 0:
        yIntercept1 = (-b-math.sqrt(sqrtValue))/(2*a)
        xIntercept1 = m*yIntercept1 + bInt
    else:
        yIntercept1 = -999
        xIntercept1 = -999

    if verbose > 9: print "intercept ", xIntercept1, yIntercept1*charge

    deltaY = yIntercept1 - yCircle
    deltaX = xIntercept1 - xCircle
    angle = -999
    
    #get angle of muon at this position if in 4th? quadrant
    if yIntercept1 != -999 and deltaY < 0 and deltaX > 0:
        angle = math.atan(deltaY/deltaX)*charge

    #see if hist the line
    hitLine = False
    #condition for hit
    if (x0-xIntercept1)*(x1-xIntercept1) < 0 and (y0-yIntercept1)*(y1-yIntercept1) < 0:
        hitLine = True


    angleChamber = math.atan(m)

    #print xIntercept1, yIntercept1*charge, angle, hitLine, (angleChamber-(pi/2-abs(angle)))*charge
    return xIntercept1, yIntercept1*charge, angle, hitLine, (angleChamber-(pi/2-abs(angle)))*charge