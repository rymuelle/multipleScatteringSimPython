import math
import random
from numba import jit
from constants import *



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